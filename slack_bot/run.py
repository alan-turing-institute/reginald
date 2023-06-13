# Standard library imports
import argparse
import logging
import os
import sys
import threading

# Third-party imports
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient

# Local imports
from slack_bot import MODELS, Bot

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", help="Select which model to use", default=None)
    args = parser.parse_args()

    # Initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # Set the model name
    model_name = os.environ.get("REGINALD_MODEL")
    if args.model:
        model_name = args.model
    if not model_name:
        model_name = "hello"

    # Initialise a new Slack bot with the requested model
    try:
        model = MODELS[model_name.lower()]
    except KeyError:
        logging.error(f"Model {model_name} was not recognised")
        sys.exit(1)

    logging.info(f"Initialising bot with model {model_name}")
    slack_bot = Bot(model())

    # Initialize SocketModeClient with an app-level token + WebClient
    client = SocketModeClient(
        # This app-level token will be used only for establishing a connection
        app_token=os.environ.get("SLACK_APP_TOKEN"),
        # You will be using this WebClient for performing Web API calls in listeners
        web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN")),
    )

    # Add a new listener to receive messages from Slack
    # You can add more listeners like this
    client.socket_mode_request_listeners.append(slack_bot)
    # Establish a WebSocket connection to the Socket Mode servers
    client.connect()

    # Listen for events
    logging.info("Listening for requests...")
    threading.Event().wait()
