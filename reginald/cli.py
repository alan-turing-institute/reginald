from typing import Optional, Annotated

import typer

from .run import main, EMOJI_DEFAULT

cli = typer.Typer()

@cli.command()
def run_all(*args) -> None:
    main(run_all=True, *args)

@cli.command()
def bot(api_url: Annotated[str, typer.Option(prompt=True)],
        emoji: str = EMOJI_DEFAULT) -> None:
    main(only_bot=True, api_url=api_url, emoji=emoji)

@cli.command()
def app(*args) -> None:
    main(only_reginald=True, *args)
