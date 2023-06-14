from __future__ import annotations

# Standard library imports
import logging
import pathlib
import re

# Third-party imports
import accelerate
import pandas as pd
import torch
import transformers
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from llama_index import (
    Document,
    LangchainEmbedding,
    LLMPredictor,
    PromptHelper,
    ServiceContext,
)
from llama_index.indices.vector_store.base import GPTVectorStoreIndex
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)

# Local imports
from .base import MessageResponse, ResponseModel

QUANTIZATION_CONFIG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)


DATA_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "data"
# TOD Leaving out the wiki for now while we figure out if we are okay sending it to
# OpenAI.
DATA_FILES = [DATA_DIR / "handbook-scraped.csv"]  # , DATA_DIR / "wiki-scraped.csv"]
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
    def _prep_documents(self):
        # Prep the contextual documents
        documents = []
        for data_file in DATA_FILES:
            df = pd.read_csv(data_file)
            df = df[~df.loc[:, "body"].isna()]
            documents += [
                Document(row[1]["body"], extra_info={"filename": row[1]["url"]})
                for row in df.iterrows()
            ]
        return documents

    def _prep_llm_predictor(self):
        raise NotImplemented(
            "_prep_llm_predictor needs to be implemented by a subclass of Llama."
        )

    def __init__(
        self,
        model_name,
        max_input_size,
        num_output=512,
        chunk_size_limit=300,
        chunk_overlap_ratio=0.1,
    ):
        logging.info("Setting up Huggingface backend.")
        self.max_input_size = max_input_size
        self.model_name = model_name
        self.num_output = num_output
        self.chunk_size_limit = chunk_size_limit
        self.chunk_overlap_ratio = chunk_overlap_ratio

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
        )

        self.index = GPTVectorStoreIndex.from_documents(
            documents, service_context=service_context
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
                + "\n\n\nCitations:\n"
                + ("-" * 50)
                + "\n"
                + query_response.get_formatted_sources()
            )
        except Exception as e:  # ignore: broad-except
            response = self.error_response_template.format(repr(e))
        pattern = (
            r"(?s)^Context information is"
            r".*"
            r"Given the context information and not prior knowledge, "
            "answer the question:"
            rf" {msg_in}"
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
        accelerator = accelerate.Accelerator()
        device = accelerator.device

        # Create the model object
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model_kwargs = (
            {"quantization_config": QUANTIZATION_CONFIG, "device_map": "auto"}
            if QUANTIZE
            else {}
        )
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name, trust_remote_code=True, **model_kwargs
        )
        model_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            # TODO Commenting this in breaks on M1.
            # device=device if not QUANTIZE else None,
        )

        llm_predictor = LLMPredictor(
            llm=CustomLLM(model_name=self.model_name, pipeline=model_pipeline)
        )
        return llm_predictor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="distilgpt2", max_input_size=1024, **kwargs)


class LlamaGPT35Turbo(Llama):
    def _prep_llm_predictor(self):
        llm_predictor = LLMPredictor(
            llm=ChatOpenAI(
                temperature=0.7, model=self.model_name, max_tokens=self.num_output
            )
        )
        return llm_predictor

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, model_name="gpt-3.5-turbo", max_input_size=4096, **kwargs
        )
