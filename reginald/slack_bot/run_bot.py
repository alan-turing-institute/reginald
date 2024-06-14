import logging
import sys

from reginald.slack_bot.utils import (
    connect_client,
    setup_api_slack_bot,
    setup_slack_client,
)


async def run_bot(
    slack_app_token: str, slack_bot_token: str, api_url: str | None, emoji: str | None
) -> None:
    if api_url is None:
        logging.error("api_url is not set.")
        sys.exit(1)

    # set up slack bot
    bot = setup_api_slack_bot(api_url=api_url, emoji=emoji)

    # set up slack client
    client = setup_slack_client(
        slack_bot=bot, slack_app_token=slack_app_token, slack_bot_token=slack_bot_token
    )

    await connect_client(client)
