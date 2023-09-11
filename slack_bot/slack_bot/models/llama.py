from __future__ import annotations

import logging
import math
import os
import pathlib
import re
from typing import Any, List, Optional

import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import (
    Document,
    PromptHelper,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.indices.vector_store.base import VectorStoreIndex
from llama_index.llms import LLM, AzureOpenAI, HuggingFaceLLM, OpenAI
from llama_index.response.schema import RESPONSE_TYPE

from .base import MessageResponse, ResponseModel

LLAMA_INDEX_DIR = "llama_index_indices"
PUBLIC_DATA_DIR = "public"
INTERNAL_DATA_DIR = "turing_internal"


class Llama(ResponseModel):
    def __init__(
        self,
        model_name: str,
        max_input_size: int,
        data_dir: pathlib.Path,
        which_index: str,
        context_window: int = 1024,
        chunk_size_limit: Optional[int] = None,
        k: int = 3,
        chunk_overlap_ratio: float = 0.1,
        force_new_index: bool = False,
        num_output: int = 256,
    ) -> None:
        super().__init__(emoji="llama")
        logging.info("Setting up Huggingface backend.")
        self.max_input_size = max_input_size
        self.model_name = model_name
        self.context_window = context_window
        self.num_output = num_output
        if chunk_size_limit is None:
            chunk_size_limit = math.ceil(max_input_size / k)
        self.chunk_size_limit = chunk_size_limit
        self.chunk_overlap_ratio = chunk_overlap_ratio
        self.data_dir = data_dir
        self.which_index = which_index

        # set up LLM
        llm = self._prep_llm()

        # initialise embedding model to use to create the index vectors
        embed_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        # construct the prompt helper
        prompt_helper = PromptHelper(
            context_window=self.max_input_size,
            num_output=self.num_output,
            chunk_size_limit=self.chunk_size_limit,
            chunk_overlap_ratio=self.chunk_overlap_ratio,
        )

        # construct the service context
        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            prompt_helper=prompt_helper,
            chunk_size_limit=chunk_size_limit,
        )

        if force_new_index:
            logging.info("Generating the index from scratch...")
            documents = self._prep_documents()
            self.index = VectorStoreIndex.from_documents(
                documents, service_context=service_context
            )

            # Save the service context and persist the index
            logging.info("Saving the index")
            self.index.storage_context.persist(
                persist_dir=self.data_dir / LLAMA_INDEX_DIR / which_index
            )

        else:
            logging.info("Loading the storage context")
            storage_context = StorageContext.from_defaults(
                persist_dir=self.data_dir / LLAMA_INDEX_DIR / which_index
            )

            logging.info("Loading the pre-processed index")
            self.index = load_index_from_storage(
                storage_context=storage_context, service_context=service_context
            )

        self.query_engine = self.index.as_query_engine(similarity_top_k=3)
        logging.info("Done setting up Huggingface backend for query engine.")

        self.error_response_template = (
            "Oh no! When I tried to get a response to your prompt, "
            "I got the following error:"
            "\n```\n{}\n```"
        )

    @staticmethod
    def _format_sources(response: RESPONSE_TYPE) -> str:
        texts = []
        for source_node in response.source_nodes:
            source_text = (
                source_node.node.extra_info["filename"]
                + f" (similarity: {round(source_node.score, 3)})"
            )
            texts.append(source_text)
        result = "I read the following documents to compose this answer:\n"
        result += "\n\n".join(texts)
        return result

    def _get_response(self, msg_in: str, user_id: str) -> str:
        try:
            query_response = self.query_engine.query(msg_in)
            # concatenate the response with the resources that it used
            response = (
                query_response.response
                + "\n\n\n"
                + self._format_sources(query_response)
            )
        except Exception as e:  # ignore: broad-except
            response = self.error_response_template.format(repr(e))
        pattern = (
            r"(?s)^Context information is"
            r".*"
            r"Given the context information and not prior knowledge, answer the question: "
            rf"{msg_in}"
            r"\n(.*)"
        )
        m = re.search(pattern, response)
        if m:
            answer = m.group(1)
        else:
            logging.warning(
                "Was expecting a backend response with a regular expression but couldn't find a match."
            )
            answer = response
        return answer

    def _prep_documents(self) -> List[Document]:
        # Prep the contextual documents
        documents = []

        if self.which_index == "handbook":
            logging.info("Regenerating index only for the handbook")

            data_files = [self.data_dir / PUBLIC_DATA_DIR / "handbook-scraped.csv"]

        elif self.which_index == "public":
            logging.info("Regenerating index for all PUBLIC. Will take a long time...")

            # pull out public data
            data_files = list((self.data_dir / PUBLIC_DATA_DIR).glob("**/*.md"))
            data_files += list((self.data_dir / PUBLIC_DATA_DIR).glob("**/*.csv"))
            data_files += list((self.data_dir / PUBLIC_DATA_DIR).glob("**/*.txt"))
        elif self.which_index == "all_data":
            logging.info("Regenerating index for ALL DATA. Will take a long time...")

            # pull out public data
            data_files = list((self.data_dir / PUBLIC_DATA_DIR).glob("**/*.md"))
            data_files += list((self.data_dir / PUBLIC_DATA_DIR).glob("**/*.csv"))
            data_files += list((self.data_dir / PUBLIC_DATA_DIR).glob("**/*.txt"))
            # include private internal data
            data_files += list((self.data_dir / INTERNAL_DATA_DIR).glob("**/*.md"))
            data_files += list((self.data_dir / INTERNAL_DATA_DIR).glob("**/*.csv"))
            data_files += list((self.data_dir / INTERNAL_DATA_DIR).glob("**/*.txt"))

        else:
            logging.info("The data_files directory is unrecognized")

        for data_file in data_files:
            if data_file.suffix == ".csv":
                df = pd.read_csv(data_file)
                df = df[~df.loc[:, "body"].isna()]
                documents += [
                    Document(row[1]["body"], extra_info={"filename": row[1]["url"]})
                    for row in df.iterrows()
                ]
            elif data_file.suffix in (".md", ".txt"):
                with open(data_file, "r") as f:
                    content = f.read()
                documents.append(
                    Document(content, extra_info={"filename": str(data_file)})
                )
        return documents

    def _prep_llm(self) -> LLM:
        raise NotImplemented(
            "_prep_llm needs to be implemented by a subclass of Llama."
        )

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        backend_response = self._get_response(message, user_id)
        return MessageResponse(backend_response)

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        backend_response = self._get_response(message, user_id)
        return MessageResponse(backend_response)


class LlamaHuggingFace(Llama):
    def __init__(
        self, model_name: str = "distilgpt2", *args: Any, **kwargs: Any
    ) -> LLM:
        super().__init__(
            *args, model_name=model_name, max_input_size=self.num_output, **kwargs
        )

    def _prep_llm(self) -> LLM:
        return HuggingFaceLLM(
            context_window=self.context_window,
            max_new_tokens=self.num_output,
            tokenizer_name=self.model_name,
            model_name=self.model_name,
            device_map="auto",
        )


class LlamaGPT35TurboOpenAI(Llama):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = 0.7
        super().__init__(
            *args, model_name="gpt-3.5-turbo-16k", max_input_size=16384, **kwargs
        )

    def _prep_llm(self) -> LLM:
        return OpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.num_output,
            api_key=self.openai_api_key,
        )


class LlamaGPT35TurboAzure(Llama):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.deployment_name = "reginald-azure-gpt35-turbo"
        self.openai_api_base = os.getenv("OPENAI_AZURE_API_BASE")
        self.openai_api_key = os.getenv("OPENAI_AZURE_API_KEY")
        self.openai_api_version = "2023-03-15-preview"
        self.temperature = 0.7
        super().__init__(
            *args, model_name="gpt-3.5-turbo-16k", max_input_size=16384, **kwargs
        )

    def _prep_llm(self) -> LLM:
        return AzureOpenAI(
            model=self.model_name,
            engine=self.deployment_name,
            temperature=self.temperature,
            max_tokens=self.num_output,
            api_key=self.openai_api_key,
            api_base=self.openai_api_base,
            api_type="azure",
            api_version=self.openai_api_version,
        )
