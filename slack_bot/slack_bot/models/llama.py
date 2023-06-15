from __future__ import annotations

# Standard library imports
import logging
import os
import pathlib
import re

# Third-party imports
import pandas as pd
import transformers
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from llama_index import (
    Document,
    LangchainEmbedding,
    LLMPredictor,
    PromptHelper,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.indices.vector_store.base import GPTVectorStoreIndex
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Local imports
from .base import MessageResponse, ResponseModel

# TOD Leaving out the wiki for now while we figure out if we are okay sending it to
# OpenAI.

LLAMA_INDEX_DIR = "llama_index_indices"
QUANTIZE = False  # Doesn't work on M1


class CustomLLM(LLM):
    model_name: str
    pipeline: transformers.pipelines.text_generation.TextGenerationPipeline

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt, stop=None):
        return self.pipeline(prompt, max_new_tokens=9999)[0]["generated_text"]

    @property
    def _identifying_params(self) -> dict:
        """Get the identifying parameters."""
        return {"model_name": self.model_name}


class Llama(ResponseModel):
    @staticmethod
    def _format_sources(response):
        texts = []
        for source_node in response.source_nodes:
            source_text = (
                source_node.node.extra_info["filename"]
                + f" (similarity: {source_node.score})"
            )
            texts.append(source_text)
        result = "I read the following documents to compose this answer:\n"
        result += "\n\n".join(texts)
        return result

    def _prep_documents(self):
        # Prep the contextual documents
        documents = []
        data_files = [self.data_dir / "handbook-scraped.csv"]

        for data_file in data_files:
            if data_file.suffix == ".csv":
                df = pd.read_csv(data_file)
                df = df[~df.loc[:, "body"].isna()]
                documents += [
                    Document(row[1]["body"], extra_info={"filename": row[1]["url"]})
                    for row in df.iterrows()
                ]
            elif data_file.suffix == ".md":
                with open(data_file, "r") as f:
                    content = f.read()
                documents.append(
                    Document(content, extra_info={"filename": str(data_file)})
                )
        return documents

    def _prep_llm_predictor(self):
        raise NotImplemented(
            "_prep_llm_predictor needs to be implemented by a subclass of Llama."
        )

    def __init__(
        self,
        model_name,
        max_input_size,
        data_dir,
        which_index,
        num_output=512,
        chunk_size_limit=300,
        chunk_overlap_ratio=0.1,
        force_new_index=False,
    ):
        logging.info("Setting up Huggingface backend.")
        self.max_input_size = max_input_size
        self.model_name = model_name
        self.num_output = num_output
        self.chunk_size_limit = chunk_size_limit
        self.chunk_overlap_ratio = chunk_overlap_ratio
        self.data_dir = pathlib.Path(data_dir)

        documents = self._prep_documents()
        llm_predictor = self._prep_llm_predictor()

        hfemb = HuggingFaceEmbeddings()
        embed_model = LangchainEmbedding(hfemb)

        prompt_helper = PromptHelper(
            context_window=self.max_input_size,
            num_output=self.num_output,
            chunk_size_limit=self.chunk_size_limit,
            chunk_overlap_ratio=self.chunk_overlap_ratio,
        )

        service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor,
            embed_model=embed_model,
            prompt_helper=prompt_helper,
            chunk_size_limit=chunk_size_limit,
        )

        logging.info(f"Load index is: {force_new_index}")

        if not force_new_index:

            logging.info("loading the pre-processed index!")

            logging.info("Generating the storage context")

            storage_context = StorageContext.from_defaults(
                persist_dir=self.data_dir / LLAMA_INDEX_DIR / which_index
            )

            logging.info("Loading the index")

            self.index = load_index_from_storage(
                storage_context=storage_context, service_context=service_context
            )

        else:

            logging.info("Generating the index anew")

            self.index = GPTVectorStoreIndex.from_documents(
                documents, service_context=service_context
            )

            logging.info("Saving the index...")

            # Save the service context and persist the index
            self.index.storage_context.persist(
                persist_dir=self.data_dir / LLAMA_INDEX_DIR / which_index
            )

        self.query_engine = self.index.as_query_engine()
        logging.info("Done setting up Huggingface backend.")

        self.error_response_template = (
            "Oh no! When I tried to get a response to your prompt, "
            "I got the following error:"
            "\n```\n{}\n```"
        )

    def _get_response(self, msg_in: str, user_id: str) -> str:
        msg_out = f"<@{user_id}>, you asked me: {msg_in}\n"
        try:
            query_response = self.query_engine.query(msg_in)
            # concatenate the response with the reources that it used
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
            r"Given the context information and not prior knowledge, "
            "answer the question: "
            rf"{msg_in}"
            r"\n(.*)"
        )
        m = re.search(pattern, response)
        if m:
            answer = m.group(1)
        else:
            logging.warning(
                "Was expecting a backend response with a regular expression "
                "but couldn't find a match."
            )
            answer = response
        msg_out += answer
        return msg_out

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        backend_response = self._get_response(message, user_id)
        return MessageResponse(backend_response, None)

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        backend_response = self._get_response(message, user_id)
        return MessageResponse(backend_response, None)


class LlamaDistilGPT2(Llama):
    def _prep_llm_predictor(self):
        # Use open-source LLM from transformers
        # Decide what device to use
        # accelerator = accelerate.Accelerator()
        # device = accelerator.device

        # Create the model object
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )
        model_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            # TODO Commenting this in breaks on M1.
            # device=device,
        )

        llm_predictor = LLMPredictor(
            llm=CustomLLM(model_name=self.model_name, pipeline=model_pipeline)
        )
        return llm_predictor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="distilgpt2", max_input_size=1024, **kwargs)


class LlamaGPT35TurboOpenAI(Llama):
    def __init__(self, *args, **kwargs):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        super().__init__(
            *args, model_name="gpt-3.5-turbo", max_input_size=4096, **kwargs
        )

    def _prep_llm_predictor(self):
        llm_predictor = LLMPredictor(
            llm=ChatOpenAI(
                max_tokens=self.num_output,
                model=self.model_name,
                openai_api_key=self.openai_api_key,
                temperature=0.7,
            )
        )
        return llm_predictor


class LlamaGPT35TurboAzure(Llama):
    def __init__(self, *args, **kwargs):
        self.deployment_name = "reginald-gpt35-turbo"
        self.openai_api_base = os.getenv("OPENAI_AZURE_API_BASE")
        self.openai_api_key = os.getenv("OPENAI_AZURE_API_KEY")
        self.openai_api_version = "2023-03-15-preview"
        self.temperature = 0.7
        super().__init__(
            *args, model_name="gpt-3.5-turbo", max_input_size=4096, **kwargs
        )

    def _prep_llm_predictor(self):
        llm_predictor = LLMPredictor(
            llm=AzureChatOpenAI(
                deployment_name=self.deployment_name,
                temperature=self.temperature,
                model=self.model_name,
                max_tokens=self.num_output,
                openai_api_key=self.openai_api_key,
                openai_api_base=self.openai_api_base,
                openai_api_version=self.openai_api_version,
                openai_api_type="azure",
            )
        )
        return llm_predictor
