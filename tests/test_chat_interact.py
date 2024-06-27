import builtins
from unittest import mock

import pytest
from typer.testing import CliRunner

from reginald.cli import cli
from reginald.models.chat_interact import (
    ART,
    CLEAR_HISTORY_STRS,
    EXIT_STRS,
    INPUT_PROMPT,
    REGINALD_PROMPT,
    run_chat_interact,
)
from reginald.models.simple.hello import Hello

runner = CliRunner()
art_split = ART.splitlines()


def test_chat_cli():
    """Test sending an input `str` via `cli` and then exiting."""
    result = runner.invoke(cli, ["chat"], input="What's up dock?\nexit\n")
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[: len(art_split)] == art_split
    assert term_stdout_lines[len(art_split) + 1] == INPUT_PROMPT
    assert (
        term_stdout_lines[len(art_split) + 2] == f"{REGINALD_PROMPT}Hello! How are you?"
    )
    assert term_stdout_lines[len(art_split) + 3] == INPUT_PROMPT


def test_chat_cli_no_stream():
    """Test sending an input `str` via `cli` and then exiting."""
    result = runner.invoke(
        cli, ["chat", "--no-streaming"], input="What's up dock?\nexit\n"
    )
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[: len(art_split)] == art_split
    assert term_stdout_lines[len(art_split) + 1] == INPUT_PROMPT
    assert (
        term_stdout_lines[len(art_split) + 2]
        == f"{REGINALD_PROMPT}Let's discuss this in a channel!"
    )
    assert term_stdout_lines[len(art_split) + 3] == INPUT_PROMPT


@pytest.mark.parametrize("input", EXIT_STRS)
def test_chat_interact_exit(input: str):
    with mock.patch.object(builtins, "input", lambda _: input):
        interaction = run_chat_interact(model="hello")
    assert isinstance(interaction, Hello)


@pytest.mark.parametrize("input", CLEAR_HISTORY_STRS)
def test_chat_interact_clear_history(input: str):
    result = runner.invoke(cli, ["chat"], input=input)
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[: len(art_split)] == art_split
    assert term_stdout_lines[len(art_split) + 1] == INPUT_PROMPT
    assert (
        term_stdout_lines[len(art_split) + 2]
        == f"{REGINALD_PROMPT}No history to clear."
    )
    assert term_stdout_lines[len(art_split) + 3] == INPUT_PROMPT
