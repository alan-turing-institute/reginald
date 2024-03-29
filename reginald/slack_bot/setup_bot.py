import argparse
import asyncio
import logging
import os
import sys

from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.web.async_client import AsyncWebClient

from reginald.models.models.base import ResponseModel
from reginald.parser_utils import get_args
from reginald.slack_bot.bot import ApiBot, Bot
from reginald.utils import get_env_var


def setup_slack_bot(model: ResponseModel) -> Bot:
    """
    Initialise `Bot` with response model.

    Parameters
    ----------
    model : ResponseModel
        Response model to use for the bot

    Returns
    -------
    Bot
        Bot with response model
    """
    logging.info(f"Initalising bot with model: {model}")

    slack_bot = Bot(model=model)

    logging.info("Connecting to Slack...")
    if get_env_var("SLACK_APP_TOKEN", log=False) is None:
        logging.error("SLACK_APP_TOKEN is not set")
        sys.exit(1)

    return slack_bot


def setup_api_slack_bot(api_url: str, emoji: str) -> ApiBot:
    """
    Initialise `ApiBot` with response model.

    Parameters
    ----------
    emoji : str
        Emoji to use for the bot for responding to messages

    Returns
    -------
    ApiBot
        Bot which uses an API for responding to messages
    """
    logging.info(f"Initalising bot at {api_url}")
    logging.info(f"Initalising bot with {emoji} emoji")

    # set up bot with the api_url and emoji
    slack_bot = ApiBot(api_url=api_url, emoji=emoji)

    logging.info("Connecting to Slack...")
    if get_env_var("SLACK_APP_TOKEN", log=False) is None:
        logging.error("SLACK_APP_TOKEN is not set")
        sys.exit(1)

    return slack_bot


def setup_slack_client(slack_bot: ApiBot | Bot) -> SocketModeClient:
    """
    Initialise Slack client with bot.

    Parameters
    ----------
    slack_bot : ApiBot | Bot
        Bot to use for responding to messages.
        This can be either an ApiBot object
        (a bot which uses an API for responding)
        or a Bot object (a bot which uses a response
        model object directly for responding)

    Returns
    -------
    SocketModeClient
        Slack client with bot
    """
    slack_app_token = get_env_var("SLACK_APP_TOKEN")
    if slack_app_token is None:
        logging.error("SLACK_APP_TOKEN is not set")
        sys.exit(1)

    slack_bot_token = get_env_var("SLACK_BOT_TOKEN")
    if slack_bot_token is None:
        logging.error("SLACK_BOT_TOKEN is not set")
        sys.exit(1)

    # initialize SocketModeClient with an app-level token + AsyncWebClient
    client = SocketModeClient(
        # this app-level token will be used only for establishing a connection
        app_token=slack_app_token,
        # you will be using this AsyncWebClient for performing Web API calls in listeners
        web_client=AsyncWebClient(token=slack_bot_token),
        # to ensure connection doesn't go stale - we can adjust as needed.
        ping_interval=60,
    )

    # add a new listener to receive messages from Slack
    client.socket_mode_request_listeners.append(slack_bot)

    return client


async def main():
    """
    Main function to run the Slack bot which sets up the bot
    (which uses an API for responding to messages) and
    then establishes a WebSocket connection to the
    Socket Mode servers and listens for events.
    """
    # initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-url",
        "-a",
        type=str,
        help=(
            "Select the API URL for the model. If not set, "
            "must be set as the REGINALD_API_URL environment variable"
        ),
        default=lambda: get_env_var("REGINALD_API_URL"),
    )
    parser.add_argument(
        "--emoji",
        "-e",
        type=str,
        help=(
            "Select the emoji for the model. By default, looks for the REGINALD_EMOJI "
            "environment variable or uses the rocket emoji"
        ),
        default=lambda: get_env_var("REGINALD_EMOJI", secret_value=False) or "rocket",
    )
    args = get_args(parser)

    if args.api_url is None:
        logging.error(
            "API URL is not set. Please set the REGINALD_API_URL "
            "environment variable or pass in the --api-url argument"
        )
        sys.exit(1)

    # set up slack bot
    bot = setup_api_slack_bot(api_url=args.api_url, emoji=args.emoji)

    # set up slack client
    client = setup_slack_client(slack_bot=bot)

    # establish a WebSocket connection to the Socket Mode servers
    await client.connect()

    # listen for events
    logging.info("Listening for requests...")
    await asyncio.sleep(float("inf"))


if __name__ == "__main__":
    asyncio.run(main())


def cli():
    asyncio.run(main())
