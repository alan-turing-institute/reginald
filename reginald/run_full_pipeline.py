from reginald.models.setup_llm import setup_llm
from reginald.slack_bot.utils import connect_client, setup_slack_bot, setup_slack_client


async def run_full_pipeline(
    slack_app_token: str, slack_bot_token: str, **kwargs
) -> None:
    # set up response model
    response_model = setup_llm(**kwargs)
    bot = setup_slack_bot(response_model)

    # set up slack client
    client = setup_slack_client(
        slack_bot=bot, slack_app_token=slack_app_token, slack_bot_token=slack_bot_token
    )

    await connect_client(client)
