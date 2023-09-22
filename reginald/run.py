import argparse
import asyncio
import logging
import os

from slack_bot.setup_bot import setup_slack_bot, setup_slack_client

API_URL = "http://127.0.0.1:8000"


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

    # TODO: add some model init stuff

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
