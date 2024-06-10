import asyncio
import logging
from typing import Final
from slack_sdk.socket_mode.aiohttp import SocketModeClient

from fastapi import FastAPI
import uvicorn

from reginald.models.setup_llm import setup_llm
from reginald.models.app import create_reginald_app 
from reginald.slack_bot.setup_bot import setup_slack_bot, setup_slack_client, EMOJI_DEFAULT, setup_api_slack_bot


LISTENING_MSG: Final[str] = "Listening for requests..." 

logging.basicConfig(
    datefmt=r"%Y-%m-%d %H:%M:%S",
    format="%(asctime)s [%(levelname)8s] %(message)s",
    level=logging.INFO,
)

async def run_bot(api_url: str | None = None, emoji: str = EMOJI_DEFAULT):

    # set up slack bot
    bot = setup_api_slack_bot(api_url=api_url, emoji=emoji)

    # set up slack client
    client = setup_slack_client(slack_bot=bot)
    await connect_client(client)


async def run_reginald_app(*args) -> None:
    # set up response model
    response_model = setup_llm(**vars(args))
    app: FastAPI = create_reginald_app(response_model)
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # return response

async def run_full_pipeline(*args):
    # set up response model
    response_model = setup_llm(**vars(args))
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
        run_all: bool = True,
        only_bot: bool = False,
        only_reginald: bool = False, api_url: str | None = None, emoji: str = EMOJI_DEFAULT, *args, **kwrags):
    # initialise logging
    if run_all:
        asyncio.run(run_full_pipeline(*args))
    elif only_bot:
        asyncio.run(run_bot(api_url=api_url, emoji=emoji))
    elif only_reginald:
        asyncio.run(run_reginald_app(*args))
    else:
        logging.info("No run options selected.")

if __name__ == "__main__":
    main()
