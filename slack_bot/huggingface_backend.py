import logging
import re

import accelerate
import pandas as pd
import torch
import transformers
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from llama_index import (
    AutoTokenizer,
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


def set_up_query_engine(data_files, model_name):
    logging.info("Setting up Huggingface backend.")
    # Prep the contextual documents
    documents = []
    for data_file in data_files:
        df = pd.read_csv(data_file)
        text_list = df["content"]
        documents += [Document(t) for t in text_list]

    # Decide what device to use
    accelerator = accelerate.Accelerator()
    device = accelerator.device

    # Create the model object
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model_pipeline = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=tokenizer,
        device=device,
        trust_remote_code=True,
    )

    llm_predictor = LLMPredictor(
        llm=CustomLLM(model_name=model_name, pipeline=model_pipeline)
    )
    hfemb = HuggingFaceEmbeddings()
    embed_model = LangchainEmbedding(hfemb)

    # set number of output tokens
    num_output = 512
    # set maximum input size
    max_input_size = 1024
    # set maximum chunk overlap
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(
        context_window=max_input_size,
        num_output=num_output,
        chunk_size_limit=chunk_size_limit,
        max_chunk_overlap=max_chunk_overlap,
    )

    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        embed_model=embed_model,
        prompt_helper=prompt_helper,
    )

    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )
    query_engine = index.as_query_engine()
    logging.info("Done setting up Huggingface backend.")
    return query_engine


QUERY_ENGINE = set_up_query_engine(
    data_file=["../data/handbook-scraped.csv", "../data/wiki-scraped.csv"],
    model_name="distilgpt2",
)
ERROR_RESPONSE_TEMPLATE = """
Oh no! When I tried to get a response to your prompt, I got the following error:
```
{}
```
"""


def call_and_response(msg_in: str, user_id: str) -> str:
    msg_out = "<@{user_id}>, you asked me: {msg_in}\n"
    try:
        response = QUERY_ENGINE.query(msg).response
    except Exception as e:  # ignore: broad-except
        response = ERROR_RESPONSE_TEMPLATE.format(repr(e))
    pattern = (
        r"(?s)^Context information is"
        r".*"
        r"Given the context information and not prior knowledge, answer the question:"
        rf" {msg_in}"
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
    msg_out += answer
    return msg_out
