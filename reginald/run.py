import asyncio
import logging
import sys
from typing import Final

import uvicorn
from fastapi import FastAPI
from slack_sdk.socket_mode.aiohttp import SocketModeClient

from reginald.models.app import create_reginald_app
from reginald.models.create_index import create_index
from reginald.models.setup_llm import setup_llm
from reginald.slack_bot.setup_bot import (
    EMOJI_DEFAULT,
    setup_api_slack_bot,
    setup_slack_bot,
    setup_slack_client,
)

LISTENING_MSG: Final[str] = "Listening for requests..."

logging.basicConfig(
    datefmt=r"%Y-%m-%d %H:%M:%S",
    format="%(asctime)s [%(levelname)8s] %(message)s",
    level=logging.INFO,
)


async def run_bot(api_url: str | None, emoji: str):
    if api_url is None:
        logging.error(
            "API URL is not set. Please set the REGINALD_API_URL "
            "environment variable or pass in the --api-url argument"
        )
        sys.exit(1)

    # set up slack bot
    bot = setup_api_slack_bot(api_url=api_url, emoji=emoji)

    # set up slack client
    client = setup_slack_client(slack_bot=bot)
    await connect_client(client)


async def run_reginald_app(**kwargs) -> None:
    # set up response model
    response_model = setup_llm(**kwargs)
    app: FastAPI = create_reginald_app(response_model)
    uvicorn.run(app, host="0.0.0.0", port=8000)


async def run_full_pipeline(**kwargs):
    # set up response model
    response_model = setup_llm(**kwargs)
    bot = setup_slack_bot(response_model)
    # set up slack client
    client = setup_slack_client(bot)
    await connect_client(client)


async def connect_client(client: SocketModeClient):
    await client.connect()
    # listen for events
    logging.info(LISTENING_MSG)
    # TODO: Assess whether this is best to use
    await asyncio.sleep(float("inf"))


def main(
    cli: str, api_url: str | None = None, emoji: str = EMOJI_DEFAULT, *args, **kwrags
):
    # initialise logging
    if cli == "run_all":
        asyncio.run(run_full_pipeline(**kwrags))
    elif cli == "bot":
        asyncio.run(run_bot(api_url=api_url, emoji=emoji))
    elif cli == "app":
        asyncio.run(run_reginald_app(**kwrags))
    elif cli == "create_index":
        create_index(**kwrags)
    else:
        logging.info("No run options selected.")


if __name__ == "__main__":
    main()
