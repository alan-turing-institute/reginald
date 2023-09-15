import argparse
import asyncio
import logging
import os
import pathlib
import sys

from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.web.async_client import AsyncWebClient

from slack_bot import MODELS, Bot

DEFAULT_LLAMA_CPP_GGUF_MODEL = (
    "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve"
    "/main/llama-2-13b-chat.Q6_K.gguf"
)
DEFAULT_HF_MODEL = "StabilityAI/stablelm-tuned-alpha-3b"


async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", "-m", help="Select which model to use", default=None, choices=MODELS
    )
    parser.add_argument(
        "--model-name",
        "-n",
        type=str,
        help=(
            "Select which LlamaCPP or HuggingFace model to use "
            "(ignored if not using llama-index-llama-cpp or llama-index-hf). "
            "Default model for llama-index-llama-cpp is downloaded from "
            f"{DEFAULT_LLAMA_CPP_GGUF_MODEL}. "
            "Default model for llama-index-hf is downloaded from "
            f"{DEFAULT_HF_MODEL}."
        ),
        default=None,
    )
    parser.add_argument(
        "--mode",
        type=str,
        help=(
            "Select which mode to use "
            "(ignored if not using llama-index-llama-cpp or llama-index-hf). "
            "Default is 'chat'."
        ),
        default=None,
        choices=["chat", "query"],
    )
    parser.add_argument(
        "--path",
        "-p",
        help=(
            "Whether or not the model_name passed is a path to the model "
            "(ignored if not using llama-index-llama-cpp)"
        ),
        action="store_true",
    )
    parser.add_argument(
        "--max-input-size",
        "-max",
        type=int,
        help=(
            "Select maximum input size for LlamaCPP or HuggingFace model "
            "(ignored if not using llama-index-llama-cpp or llama-index-hf)"
        ),
        default=4096,
    )
    parser.add_argument(
        "--n-gpu-layers",
        "-ngl",
        type=int,
        help=(
            "Select number of GPU layers for LlamaCPP model "
            "(ignored if not using llama-index-llama-cpp)"
        ),
        default=0,
    )
    parser.add_argument(
        "--device",
        "-dev",
        type=str,
        help=(
            "Select device for HuggingFace model "
            "(ignored if not using llama-index-hf model)"
        ),
        default="auto",
    )
    parser.add_argument(
        "--force-new-index",
        "-f",
        help="Recreate the index vector store or not",
        action="store_true",
    )
    parser.add_argument(
        "--data-dir",
        "-d",
        type=pathlib.Path,
        help="Location for data",
        default=None,
    )
    parser.add_argument(
        "--which-index",
        "-w",
        type=str,
        help=(
            "Specifies the directory name for looking up/writing indices. "
            "Currently supports 'all_data', 'public' and 'handbook'. "
            "If regenerating index, 'all_data' will use all .txt .md. and .csv "
            "files in the data directory, 'handbook' will "
            "only use 'handbook.csv' file."
        ),
        default=None,
        choices=["all_data", "public", "handbook"],
    )

    args = parser.parse_args()

    # Initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # Set model name
    model_name = os.environ.get("REGINALD_MODEL")
    if args.model:
        model_name = args.model
    if not model_name:
        model_name = "hello"

    # Set force new index
    force_new_index = False
    if os.environ.get("LLAMA_FORCE_NEW_INDEX"):
        force_new_index = os.environ.get("LLAMA_FORCE_NEW_INDEX").lower() == "true"
    if args.force_new_index:
        force_new_index = True

    # Set data directory
    data_dir = os.environ.get("LLAMA_DATA_DIR")
    if args.data_dir:
        data_dir = args.data_dir
    if not data_dir:
        data_dir = pathlib.Path(__file__).parent.parent / "data"
    data_dir = pathlib.Path(data_dir).resolve()

    # Set which index
    which_index = os.environ.get("LLAMA_WHICH_INDEX")
    if args.which_index:
        which_index = args.which_index
    if not which_index:
        which_index = "all_data"

    # Set mode
    mode = os.environ.get("LLAMA_MODE")
    if args.mode:
        mode = args.mode
    if not mode:
        mode = "chat"

    # Initialise a new Slack bot with the requested model
    try:
        model = MODELS[model_name.lower()]
    except KeyError:
        logging.error(f"Model {model_name} was not recognised")
        sys.exit(1)

    # Initialise LLM reponse model
    logging.info(f"Initialising bot with model: {model_name}")

    # Set up any model args that are required
    if model_name == "llama-index-llama-cpp":
        if args.model_name is None:
            args.model_name = DEFAULT_LLAMA_CPP_GGUF_MODEL

        model_args = {
            "model_name": args.model_name,
            "path": args.path,
            "n_gpu_layers": args.n_gpu_layers,
            "max_input_size": args.max_input_size,
        }
    elif model_name == "llama-index-hf":
        if args.model_name is None:
            args.model_name = DEFAULT_HF_MODEL

        model_args = {
            "model_name": args.model_name,
            "device": args.device,
            "max_input_size": args.max_input_size,
        }
    else:
        model_args = {}

    if model_name == "hello":
        response_model = model()
    else:
        response_model = model(
            force_new_index=force_new_index,
            data_dir=data_dir,
            which_index=which_index,
            mode=mode,
            **model_args,
        )

    # Initialise Bot with response model
    logging.info(f"Initalising bot with model: {response_model}")

    slack_bot = Bot(response_model)

    logging.info("Connecting to Slack...")
    if os.environ.get("SLACK_APP_TOKEN") is None:
        logging.error("SLACK_APP_TOKEN is not set")
        sys.exit(1)

    # Initialize SocketModeClient with an app-level token + WebClient
    client = SocketModeClient(
        # This app-level token will be used only for establishing a connection
        app_token=os.environ.get("SLACK_APP_TOKEN"),
        # You will be using this WebClient for performing Web API calls in listeners
        web_client=AsyncWebClient(token=os.environ.get("SLACK_BOT_TOKEN")),
    )

    # Add a new listener to receive messages from Slack
    client.socket_mode_request_listeners.append(slack_bot)
    # Establish a WebSocket connection to the Socket Mode servers
    await client.connect()

    # Listen for events
    logging.info("Listening for requests...")
    await asyncio.sleep(float("inf"))


if __name__ == "__main__":
    asyncio.run(main())
