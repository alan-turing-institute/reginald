import argparse
import logging
import os
import pathlib
import sys
import threading

from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient

from slack_bot import MODELS, Bot

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", "-m", help="Select which model to use", default=None, choices=MODELS
    )
    parser.add_argument(
        "--hf_model",
        "-hf",
        help="""Select which HuggingFace model to use
        (ignored if not using llama-huggingface model)""",
        default="StabilityAI/stablelm-tuned-alpha-3b",
    )
    parser.add_argument(
        "--max_input_size",
        "-max",
        help="""Select maximum input size for HuggingFace model
        (ignored if not using llama-huggingface model)""",
        default=4096,
    )
    parser.add_argument(
        "--device",
        "-dev",
        help="""Select device for HuggingFace model
        (ignored if not using llama-huggingface model)""",
        default="auto",
    )
    parser.add_argument(
        "--force-new-index",
        "-f",
        help="Recreate the index vector store or not",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--data-dir",
        "-d",
        help="Location for data",
        default=(pathlib.Path(__file__).parent.parent / "data").resolve(),
    )
    parser.add_argument(
        "--which-index",
        "-w",
        help="""Specifies the directory name for looking up/writing indices.
        Currently supports 'all_data', 'public' and 'handbook'.
        If regenerating index, 'all_data' will use all .txt .md. and .csv
        files in the data directory, 'handbook' will
        only use 'handbook.csv' file.""",
        default="all_data",
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

    # Initialise a new Slack bot with the requested model
    try:
        model = MODELS[model_name.lower()]
    except KeyError:
        logging.error(f"Model {model_name} was not recognised")
        sys.exit(1)

    logging.info(f"Initialising bot with model: {model_name}")

    if model_name == "llama-index-hf":
        response_model = model(
            model_name=args.hf_model,
            max_input_size=args.max_input_size,
            device=args.device,
            force_new_index=force_new_index,
            data_dir=data_dir,
            which_index=which_index,
        )
    else:
        response_model = model(
            force_new_index=force_new_index,
            data_dir=data_dir,
            which_index=which_index,
        )

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
        web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN")),
    )

    # Add a new listener to receive messages from Slack
    client.socket_mode_request_listeners.append(slack_bot)
    # Establish a WebSocket connection to the Socket Mode servers
    client.connect()

    # Listen for events
    logging.info("Listening for requests...")
    threading.Event().wait()
