import asyncio
import logging

from reginald.models.setup_llm import setup_llm
from reginald.parser_utils import Parser, get_args
from reginald.slack_bot.setup_bot import setup_slack_bot, setup_slack_client


async def main():
    # initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # parse command line arguments
    parser = Parser()

    # pass args to setup_llm
    args = get_args(parser)

    # set up response model
    response_model = setup_llm(**vars(args))

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
