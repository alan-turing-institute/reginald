from __future__ import annotations

import logging
import math
import os
import pathlib
import re
import sys
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
from llama_index.llms import AzureOpenAI, HuggingFaceLLM, LlamaCPP, OpenAI
from llama_index.llms.base import LLM
from llama_index.llms.llama_utils import completion_to_prompt, messages_to_prompt
from llama_index.prompts import PromptTemplate
from llama_index.response.schema import RESPONSE_TYPE

from .base import MessageResponse, ResponseModel

LLAMA_INDEX_DIR = "llama_index_indices"
PUBLIC_DATA_DIR = "public"
INTERNAL_DATA_DIR = "turing_internal"


class LlamaIndex(ResponseModel):
    def __init__(
        self,
        model_name: str,
        max_input_size: int,
        data_dir: pathlib.Path,
        which_index: str,
        chunk_size: Optional[int] = None,
        mode: str = "chat",
        k: int = 3,
        chunk_overlap_ratio: float = 0.1,
        force_new_index: bool = False,
        num_output: int = 512,
    ) -> None:
        """
        Base class for models using llama-index.
        This class is not intended to be used directly, but rather subclassed
        to implement the `_prep_llm` method which constructs the LLM to be used.

        Parameters
        ----------
        model_name : str
            Model name to specify which LLM to use.
        max_input_size : int
            Context window size for the LLM.
        data_dir : pathlib.Path
            Path to the data directory.
        which_index : str
            Which index to construct (if force_new_index is True) or use.
            Options are "handbook", "public", or "all_data".
        chunk_size : Optional[int], optional
            Maximum size of chunks to use, by default None.
            If None, this is computed as `ceil(max_input_size / k)`.
        mode : Optional[str], optional
            The type of engine to use when interacting with the data, options of "chat" or "query".
            Default is "chat".
        k : int, optional
            `similarity_top_k` to use in char or query engine, by default 3
        chunk_overlap_ratio : float, optional
            Chunk overlap as a ratio of chunk size, by default 0.1
        force_new_index : bool, optional
            Whether or not to recreate the index vector store,
            by default False
        num_output : int, optional
            Number of outputs for the LLM, by default 512
        """
        super().__init__(emoji="llama")
        logging.info("Setting up Huggingface backend.")
        if mode == "chat":
            logging.info("Setting up chat engine.")
        elif mode == "query":
            logging.info("Setting up query engine.")
        else:
            logging.error("Mode must either be 'query' or 'chat'.")
            sys.exit(1)

        self.max_input_size = max_input_size
        self.model_name = model_name
        self.num_output = num_output
        if chunk_size is None:
            chunk_size = math.ceil(max_input_size / k)
        self.mode = mode
        self.k = k
        self.chunk_size = chunk_size
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
            chunk_size_limit=self.chunk_size,
            chunk_overlap_ratio=self.chunk_overlap_ratio,
        )

        # construct the service context
        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            prompt_helper=prompt_helper,
            chunk_size=chunk_size,
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

        if self.mode == "chat":
            self.chat_engine = {}
            logging.info("Done setting up Huggingface backend for chat engine.")
        elif self.mode == "query":
            self.query_engine = {}
            logging.info("Done setting up Huggingface backend for query engine.")

        self.error_response_template = (
            "Oh no! When I tried to get a response to your prompt, "
            "I got the following error:"
            "\n```\n{}\n```"
        )

    @staticmethod
    def _format_sources(response: RESPONSE_TYPE) -> str:
        """
        Method to format the sources used to compose the response.

        Parameters
        ----------
        response : RESPONSE_TYPE
            response object from the query engine

        Returns
        -------
        str
            String containing the formatted sources that
            were used to compose the response
        """
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
        """
        Method to obtain a response from the query/chat engine given
        a message and a user id.

        Parameters
        ----------
        msg_in : str
            Message from user
        user_id : str
            User ID

        Returns
        -------
        str
            String containing the response from the query engine.
        """
        try:
            if self.mode == "chat":
                if self.chat_engine.get(user_id) is None:
                    self.chat_engine[user_id] = self.index.as_chat_engine(
                        chat_mode="context", similarity_top_k=self.k
                    )

                chat_engine = self.chat_engine[user_id]
                response = chat_engine.chat(msg_in)
            elif self.mode == "query":
                if self.query_engine.get(user_id) is None:
                    self.query_engine[user_id] = self.index.as_query_engine(
                        similarity_top_k=self.k
                    )

                query_engine = self.query_engine[user_id]
                response = query_engine.query(msg_in)

            # concatenate the response with the resources that it used
            formatted_response = (
                response.response + "\n\n\n" + self._format_sources(response)
            )
        except Exception as e:  # ignore: broad-except
            formatted_response = self.error_response_template.format(repr(e))
        pattern = (
            r"(?s)^Context information is"
            r".*"
            r"Given the context information and not prior knowledge, answer the question: "
            rf"{msg_in}"
            r"\n(.*)"
        )
        m = re.search(pattern, formatted_response)
        if m:
            answer = m.group(1)
        else:
            logging.warning(
                "Was expecting a backend response with a regular expression but couldn't find a match."
            )
            answer = formatted_response
        return answer

    def _prep_documents(self) -> List[Document]:
        """
        Method to prepare the documents for the index vector store.

        Returns
        -------
        List[Document]
            List of `llama_index.Documents` to be used to construct the index vector store.
        """
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
                    Document(
                        text=row[1]["body"], extra_info={"filename": row[1]["url"]}
                    )
                    for row in df.iterrows()
                ]
            elif data_file.suffix in (".md", ".txt"):
                with open(data_file, "r") as f:
                    content = f.read()
                documents.append(
                    Document(text=content, extra_info={"filename": str(data_file)})
                )
        return documents

    def _prep_llm(self) -> LLM:
        """
        Method to prepare the LLM to be used.

        Returns
        -------
        LLM
            LLM to be used.

        Raises
        ------
        NotImplemented
            This must be implemented by a subclass of LlamaIndex.
        """
        raise NotImplemented(
            "_prep_llm needs to be implemented by a subclass of LlamaIndex."
        )

    def respond(self, message: str, user_id: str) -> MessageResponse:
        """
        Method to respond to a direct message or channel mention in Slack.

        Parameters
        ----------
        msg_in : str
            Message from user
        user_id : str
            User ID

        Returns
        -------
        MessageResponse
            Response from the query engine.
        """
        backend_response = self._get_response(message, user_id)

        return MessageResponse(backend_response)


class LlamaIndexLlamaCPP(LlamaIndex):
    def __init__(
        self,
        model_name: str,
        is_path: bool,
        n_gpu_layers: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        `LlamaIndexLlamaCPP` is a subclass of `LlamaIndex` that uses
        llama-cpp to implement the LLM.

        Parameters
        ----------
        model_name : str
            Either the path to the model or the URL to download the model from
        is_path : bool, optional
            If True, model_name is used as a path to the model file,
            otherwise it should be the URL to download the model
        n_gpu_layers : int, optional
            Number of layers to offload to GPU.
            If -1, all layers are offloaded, by default 0
        """
        self.is_path = is_path
        self.n_gpu_layers = n_gpu_layers
        super().__init__(*args, model_name=model_name, **kwargs)

    def _prep_llm(self) -> LLM:
        logging.info(
            f"Setting up LlamaCPP LLM (model {self.model_name}) on {self.n_gpu_layers} GPU layers"
        )
        logging.info(
            f"LlamaCPP-args: (context_window: {self.max_input_size}, num_output: {self.num_output})"
        )

        return LlamaCPP(
            model_url=self.model_name if not self.is_path else None,
            model_path=self.model_name if self.is_path else None,
            temperature=0.1,
            max_new_tokens=self.num_output,
            context_window=self.max_input_size,
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            model_kwargs={"n_gpu_layers": self.n_gpu_layers},
            # transform inputs into Llama2 format
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=True,
        )


class LlamaIndexHF(LlamaIndex):
    def __init__(
        self,
        model_name: str = "StabilityAI/stablelm-tuned-alpha-3b",
        device: str = "auto",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        `LlamaIndexHF` is a subclass of `LlamaIndex` that uses HuggingFace's
        `transformers` library to implement the LLM.

        Parameters
        ----------
        model_name : str, optional
            Model name from Huggingface's model hub,
            by default "StabilityAI/stablelm-tuned-alpha-3b".
        device : str, optional
            Device map to use for the LLM, by default "auto".
        """
        self.device = device
        super().__init__(*args, model_name=model_name, **kwargs)

    def _prep_llm(self) -> LLM:
        logging.info(
            f"Setting up Huggingface LLM (model {self.model_name}) on device {self.device}"
        )
        logging.info(
            f"HF-args: (context_window: {self.max_input_size}, num_output: {self.num_output})"
        )

        return HuggingFaceLLM(
            context_window=self.max_input_size,
            max_new_tokens=self.num_output,
            # TODO: allow user to specify the query wrapper prompt for their model
            query_wrapper_prompt=PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>"),
            generate_kwargs={"temperature": 0.1, "do_sample": False},
            tokenizer_name=self.model_name,
            model_name=self.model_name,
            device_map=self.device or "auto",
        )


class LlamaIndexGPTOpenAI(LlamaIndex):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        `LlamaIndexGPTOpenAI` is a subclass of `LlamaIndex` that uses OpenAI's
        API to implement the LLM.

        Must have `OPENAI_API_KEY` set as an environment variable.
        """
        if os.getenv("OPENAI_API_KEY") is None:
            raise ValueError("You must set OPENAI_API_KEY for OpenAI.")

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = 0.7
        super().__init__(
            *args, model_name="gpt-3.5-turbo", max_input_size=4096, **kwargs
        )

    def _prep_llm(self) -> LLM:
        return OpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.num_output,
            api_key=self.openai_api_key,
        )


class LlamaIndexGPTAzure(LlamaIndex):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        `LlamaIndexGPTAzure` is a subclass of `LlamaIndex` that uses Azure's
        instance of OpenAI's LLMs to implement the LLM.

        Must have the following environment variables set:
        - `OPENAI_API_BASE`: Azure endpoint which looks
          like https://YOUR_RESOURCE_NAME.openai.azure.com/
        - `OPENAI_API_KEY`: Azure API key
        """
        if os.getenv("OPENAI_AZURE_API_BASE") is None:
            raise ValueError(
                "You must set OPENAI_AZURE_API_BASE to your Azure endpoint. "
                "It should look like https://YOUR_RESOURCE_NAME.openai.azure.com/"
            )
        if os.getenv("OPENAI_AZURE_API_KEY") is None:
            raise ValueError("You must set OPENAI_AZURE_API_KEY for Azure OpenAI.")

        # deployment name can be found in the Azure AI Studio portal
        self.deployment_name = "reginald-gpt35-turbo"
        self.openai_api_base = os.getenv("OPENAI_AZURE_API_BASE")
        self.openai_api_key = os.getenv("OPENAI_AZURE_API_KEY")
        self.openai_api_version = "2023-03-15-preview"
        self.temperature = 0.7
        super().__init__(
            *args, model_name="gpt-3.5-turbo", max_input_size=4096, **kwargs
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
