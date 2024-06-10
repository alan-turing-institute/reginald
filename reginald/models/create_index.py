import logging
import pathlib
from typing import Any

from llama_index.core.base.llms.types import (
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core.llms.custom import CustomLLM

from reginald.models.models.llama_index import (
    DataIndexCreator,
    compute_default_chunk_size,
    setup_settings,
)
from reginald.models.setup_llm import DEFAULT_ARGS


class DummyLLM(CustomLLM):
    """
    Dummy LLM for passing into the Settings below to create the index.
    The minimum required attributes are set here, but this LLM is not used anywhere else.
    """

    context_window: int = 1024
    num_output: int = 256
    model_name: str = "dummy"
    dummy_response: str = "This is a dummy model"

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        return CompletionResponse(text=self.dummy_response)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        response = ""
        for token in self.dummy_response:
            response += token
            yield CompletionResponse(text=response, delta=token)


def create_index(
    data_dir: str,
    which_index: str,
    max_input_size: int | None,
    k: int | None,
    chunk_size: int | None,
    chunk_overlap_ratio: float | None,
    num_output: int | None,
) -> None:
    max_input_size = max_input_size or DEFAULT_ARGS["max_input_size"]
    num_output = num_output or DEFAULT_ARGS["num_output"]
    chunk_overlap_ratio = chunk_overlap_ratio or DEFAULT_ARGS["chunk_overlap_ratio"]
    k = k or DEFAULT_ARGS["k"]
    chunk_size = chunk_size or compute_default_chunk_size(
        max_input_size=max_input_size, k=k
    )

    # pass args to create data index
    logging.info("Setting up settings...")
    settings = setup_settings(
        llm=DummyLLM(),
        max_input_size=max_input_size,
        num_output=num_output,
        chunk_overlap_ratio=chunk_overlap_ratio,
        chunk_size=chunk_size,
        k=k,
    )

    # set up slack bot
    logging.info("Generating the index from scratch...")
    data_creator = DataIndexCreator(
        data_dir=pathlib.Path(data_dir or DEFAULT_ARGS["data_dir"]).resolve(),
        which_index=which_index or DEFAULT_ARGS["which_index"],
        settings=settings,
    )
    data_creator.create_index()
    data_creator.save_index()
