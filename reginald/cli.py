from typing import Annotated

import typer

from reginald.run import EMOJI_DEFAULT, main
from reginald.utils import get_env_var

API_URL_PROPMPT = "No API URL was provided and REGINALD_API_URL not set. Please provide an API URL for the Reginald app"

cli = typer.Typer()


@cli.command()
def run_all(*args) -> None:
    main(cli="run_all", *args)


@cli.command()
def bot(
    api_url: Annotated[str, typer.Option(prompt=API_URL_PROPMPT)] = get_env_var(
        "REGINALD_API_URL"
    ),
    emoji: str = get_env_var("REGINALD_EMOJI", secret_value=False) or EMOJI_DEFAULT,
) -> None:
    main(
        cli="bot",
        api_url=api_url,
        emoji=emoji,
    )


@cli.command()
def app(*args) -> None:
    main(cli="app", *args)
