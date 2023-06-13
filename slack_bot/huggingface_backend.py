import logging

import pandas as pd
import torch
import transformers
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from llama_index import (
    Document,
    GPTListIndex,
    LangchainEmbedding,
    LLMPredictor,
    PromptHelper,
    ServiceContext,
    SimpleDirectoryReader,
)
from llama_index.indices.vector_store.base import GPTVectorStoreIndex
from transformers import pipeline


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


def set_up_query_engine(data_file, model_name):
    logging.info("Setting up Huggingface backend.")
    # Prep the contextual documents
    df = pd.read_csv(data_file)
    text_list = df["content"]
    documents = [Document(t) for t in text_list]

    # Create the model object
    model_pipeline = pipeline(
        "text-generation",
        model=model_name,
        model_kwargs={"torch_dtype": torch.bfloat16},
    )
    llm_predictor = LLMPredictor(
        llm=CustomLLM(model_name=model_name, pipeline=model_pipeline)
    )
    hfemb = HuggingFaceEmbeddings()
    embed_model = LangchainEmbedding(hfemb)
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, embed_model=embed_model
    )

    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )
    query_engine = index.as_query_engine()
    logging.info("Done setting up Huggingface backend.")
    return query_engine


QUERY_ENGINE = set_up_query_engine(
    data_file="../data/data-wiki.csv", model_name="distilgpt2"
)

ERROR_RESPONSE_TEMPLATE = """
Oh no! When I tried to get a response to your prompt, I got the following error:
```
{}
```
"""


def call_and_response(msg: str, user_id: str) -> str:
    try:
        response = QUERY_ENGINE.query(msg).response
    except Exception as e:  # ignore: broad-except
        response = ERROR_RESPONSE_TEMPLATE.format(repr(e))
    return response
