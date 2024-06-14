import asyncio
import logging
from typing import Final

from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.web.async_client import AsyncWebClient

from reginald.defaults import EMOJI_DEFAULT
from reginald.models.base import ResponseModel
from reginald.slack_bot.bot import ApiBot, Bot

LISTENING_MSG: Final[str] = "Listening for requests..."


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

    return slack_bot


def setup_api_slack_bot(api_url: str, emoji: str | None) -> ApiBot:
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

    if emoji is None:
        emoji = EMOJI_DEFAULT
    logging.info(f"Initalising bot with {emoji} emoji")

    # set up bot with the api_url and emoji
    slack_bot = ApiBot(api_url=api_url, emoji=emoji)

    return slack_bot


def setup_slack_client(
    slack_bot: ApiBot | Bot, slack_app_token: str, slack_bot_token: str
) -> SocketModeClient:
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
    logging.info("Connecting to Slack...")

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


async def connect_client(client: SocketModeClient) -> None:
    await client.connect()
    # listen for events
    logging.info(LISTENING_MSG)
    # TODO: Assess whether this is best to use
    await asyncio.sleep(float("inf"))
