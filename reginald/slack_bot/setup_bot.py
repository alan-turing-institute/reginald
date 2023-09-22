import argparse
import asyncio
import logging
import os
import sys

from bot import Bot
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.web.async_client import AsyncWebClient

API_URL = "http://127.0.0.1:8000"


def setup_slack_bot(emoji: str) -> Bot:
    # Initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # Initialise Bot with response model
    logging.info(f"Initalising bot at {API_URL}")
    logging.info(f"Initalising bot with {emoji} emoji")

    slack_bot = Bot(API_URL, emoji)

    logging.info("Connecting to Slack...")
    if os.environ.get("SLACK_APP_TOKEN") is None:
        logging.error("SLACK_APP_TOKEN is not set")
        sys.exit(1)

    return slack_bot


def setup_slack_client(slack_bot: Bot) -> SocketModeClient:
    # Initialize SocketModeClient with an app-level token + AsyncWebClient
    client = SocketModeClient(
        # This app-level token will be used only for establishing a connection
        app_token=os.environ.get("SLACK_APP_TOKEN"),
        # You will be using this AsyncWebClient for performing Web API calls in listeners
        web_client=AsyncWebClient(token=os.environ.get("SLACK_BOT_TOKEN")),
        # To ensure connection doesn't go stale - we can adjust as needed.
        ping_interval=60,
    )

    # Add a new listener to receive messages from Slack
    client.socket_mode_request_listeners.append(slack_bot)

    return client


async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--emoji",
        "-e",
        help="Select the emoji for the model",
        default=os.environ.get("REGINALD_EMOJI") or "rocket",
    )
    args = parser.parse_args()

    # set up slack bot
    bot = setup_slack_bot(args.emoji)

    # set up slack client
    client = setup_slack_client(bot)

    # Establish a WebSocket connection to the Socket Mode servers
    await client.connect()

    # Listen for events
    logging.info("Listening for requests...")
    await asyncio.sleep(float("inf"))


if __name__ == "__main__":
    asyncio.run(main())
