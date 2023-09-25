import argparse
import asyncio
import logging
import os
import pathlib

from reginald.models.models import MODELS
from reginald.models.setup_llm import setup_llm
from reginald.slack_bot.setup_bot import setup_slack_bot, setup_slack_client

API_URL = "http://127.0.0.1:8000"


async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()

    # model args
    parser.add_argument(
        "--model",
        "-m",
        help=("Select which type of model to use " "Default is 'hello'.",),
        default=os.environ.get("REGINALD_MODEL"),
        choices=MODELS,
    )
    parser.add_argument(
        "--model-name",
        "-n",
        type=str,
        help=(
            "Select which model to use "
            "(ignored if using 'hello' or OpenAI model types)."
        ),
        default=os.environ.get("REGINALD_MODEL_NAME"),
    )
    parser.add_argument(
        "--mode",
        type=str,
        help=(
            "Select which mode to use "
            "(ignored if not using llama-index). "
            "Default is 'chat'."
        ),
        default=os.environ.get("LLAMA_INDEX_MODE"),
        choices=["chat", "query"],
    )
    parser.add_argument(
        "--data-dir",
        "-d",
        type=pathlib.Path,
        help="Location for data",
        default=os.environ.get("LLAMA_INDEX_DATA_DIR")
        or (pathlib.Path(__file__).parent.parent / "data").resolve(),
    )
    parser.add_argument(
        "--which-index",
        "-w",
        type=str,
        help=(
            "Specifies the directory name for looking up/writing indices. "
            "Currently supports 'handbook', 'wikis', 'public', or 'all_data'. "
            "Default is 'all_data'."
        ),
        default=os.environ.get("LLAMA_INDEX_WHICH_INDEX"),
        choices=["handbook", "wikis", "public", "all_data"],
    )
    parser.add_argument(
        "--force-new-index",
        "-f",
        help="Recreate the index vector store or not",
        action=argparse.BooleanOptionalAction,
        default=os.environ.get("LLAMA_INDEX_FORCE_NEW_INDEX"),
    )
    parser.add_argument(
        "--max-input-size",
        "-max",
        type=int,
        help=(
            "Select maximum input size for LlamaCPP or HuggingFace model "
            "(ignored if not using llama-index-llama-cpp or llama-index-hf). "
            "Default is 4096."
        ),
        default=os.environ.get("LLAMA_INDEX_MAX_INPUT_SIZE"),
    )
    parser.add_argument(
        "--n-gpu-layers",
        "-ngl",
        type=int,
        help=(
            "Select number of GPU layers for LlamaCPP model "
            "(ignored if not using llama-index-llama-cpp). "
            "Default is 0."
        ),
        default=os.environ.get("LLAMA_INDEX_N_GPU_LAYERS"),
    )
    parser.add_argument(
        "--device",
        "-dev",
        type=str,
        help=(
            "Select device for HuggingFace model "
            "(ignored if not using llama-index-hf model). "
            "Default is 'auto'."
        ),
        default=os.environ.get("LLAMA_INDEX_DEVICE"),
    )

    # pass args to setup_llm
    llm_kwargs = vars(parser.parse_args())

    # set up response model
    response_model = setup_llm(**llm_kwargs)

    # set up slack bot
    bot = setup_slack_bot(response_model)

    # set up slack client
    client = setup_slack_client(bot)

    # establish a WebSocket connection to the Socket Mode servers
    await client.connect()

    # listen for events
    logging.info("Listening for requests...")
    await asyncio.sleep(float("inf"))


if __name__ == "__main__":
    asyncio.run(main())


def cli():
    asyncio.run(main())