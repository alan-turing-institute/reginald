import asyncio
import logging


def main(
    cli: str,
    api_url: str | None = None,
    emoji: str | None = None,
    streaming: bool = False,
    data_dir: str | None = None,
    which_index: str | None = None,
    slack_app_token: str | None = None,
    slack_bot_token: str | None = None,
    **kwargs,
):
    # initialise logging
    if cli == "run_all":
        from reginald.run_full_pipeline import run_full_pipeline

        asyncio.run(
            run_full_pipeline(
                data_dir=data_dir,
                which_index=which_index,
                slack_app_token=slack_app_token,
                slack_bot_token=slack_bot_token,
                **kwargs,
            )
        )
    elif cli == "bot":
        from reginald.slack_bot.run_bot import run_bot

        asyncio.run(
            run_bot(
                slack_app_token=slack_app_token,
                slack_bot_token=slack_bot_token,
                api_url=api_url,
                emoji=emoji,
            )
        )
    elif cli == "app":
        from reginald.models.app import run_reginald_app

        run_reginald_app(data_dir=data_dir, which_index=which_index, **kwargs)
    elif cli == "chat":
        import warnings

        warnings.filterwarnings("ignore")

        from reginald.models.chat_interact import run_chat_interact

        run_chat_interact(
            streaming=streaming, data_dir=data_dir, which_index=which_index, **kwargs
        )
    elif cli == "create_index":
        from reginald.models.create_index import create_index

        create_index(data_dir=data_dir, which_index=which_index, **kwargs)
    elif cli == "download":
        from reginald.models.download_from_fileshare import download_from_fileshare

        download_from_fileshare(data_dir=data_dir, which_index=which_index, **kwargs)
    else:
        logging.info("No run options selected.")


if __name__ == "__main__":
    main()
