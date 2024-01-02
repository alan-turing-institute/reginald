import logging
from typing import Any

from llama_index.llms import (
    CompletionResponse,
    CompletionResponseGen,
    CustomLLM,
    LLMMetadata,
)
from llama_index.llms.base import llm_completion_callback
from llama_index.llms.custom import CustomLLM

from reginald.models.models.llama_index import DataIndexCreator, setup_service_context
from reginald.models.setup_llm import DEFAULT_ARGS
from reginald.parser_utils import Parser, get_args


class DummyLLM(CustomLLM):
    """
    Dummy LLM for passing into the ServiceContext below to create the index.
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


def main():
    """
    Main function to create the indices for the LlamaIndex models.
    """
    # initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # parse command line arguments
    parser = Parser(create_index_only=True)

    # pass args to setup_llm
    args = get_args(parser)

    # pass args to create data index
    logging.info("Setting up service context...")
    service_context = setup_service_context(
        llm=DummyLLM(),
        max_input_size=args.max_input_size or DEFAULT_ARGS["max_input_size"],
        num_output=args.num_output or DEFAULT_ARGS["num_output"],
        chunk_size=args.chunk_size
        or int(
            (args.max_input_size or DEFAULT_ARGS["max_input_size"])
            / ((args.k or DEFAULT_ARGS["k"]) + 1)
        ),
        chunk_overlap_ratio=args.chunk_overlap_ratio
        or DEFAULT_ARGS["chunk_overlap_ratio"],
    )

    # set up slack bot
    logging.info("Generating the index from scratch...")
    data_creator = DataIndexCreator(
        data_dir=args.data_dir or DEFAULT_ARGS["data_dir"],
        which_index=args.which_index or DEFAULT_ARGS["which_index"],
        service_context=service_context,
    )
    data_creator.create_index()
    data_creator.save_index()


if __name__ == "__main__":
    main()
