import builtins
from unittest import mock

import pytest
from typer.testing import CliRunner

from reginald.cli import cli
from reginald.models.chat_interact import art, run_chat_interact
from reginald.models.simple.hello import Hello

runner = CliRunner()
art_split = art.splitlines()


def test_chat_cli():
    """Test sending an input `str` via `cli` and then exiting."""
    result = runner.invoke(cli, ["chat"], input="What's up dock?\nexit\n")
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[: len(art_split)] == art_split
    assert term_stdout_lines[len(art_split) + 1] == ">>> "
    assert term_stdout_lines[len(art_split) + 2] == "Reginald: Hello! How are you?"
    assert term_stdout_lines[len(art_split) + 3] == ">>> "


def test_chat_cli_no_stream():
    """Test sending an input `str` via `cli` and then exiting."""
    result = runner.invoke(
        cli, ["chat", "--no-streaming"], input="What's up dock?\nexit\n"
    )
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[: len(art_split)] == art_split
    assert term_stdout_lines[len(art_split) + 1] == ">>> "
    assert (
        term_stdout_lines[len(art_split) + 2]
        == "Reginald: Let's discuss this in a channel!"
    )
    assert term_stdout_lines[len(art_split) + 3] == ">>> "


def test_chat_interact_exit():
    with mock.patch.object(builtins, "input", lambda _: "exit"):
        interaction = run_chat_interact(model="hello")
    assert isinstance(interaction, Hello)


def test_chat_interact_exit_with_bracket():
    with mock.patch.object(builtins, "input", lambda _: "exit()"):
        interaction = run_chat_interact(model="hello")
    assert isinstance(interaction, Hello)


def test_chat_interact_quit_with_bracket():
    with mock.patch.object(builtins, "input", lambda _: "quit()"):
        interaction = run_chat_interact(model="hello")
    assert isinstance(interaction, Hello)


def test_chat_interact_bye():
    with mock.patch.object(builtins, "input", lambda _: "bye Reginald"):
        interaction = run_chat_interact(model="hello")
    assert isinstance(interaction, Hello)


def test_chat_interact_clear_history():
    result = runner.invoke(cli, ["chat"], input="clear_history\n")
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[: len(art_split)] == art_split
    assert term_stdout_lines[len(art_split) + 1] == ">>> "
    assert term_stdout_lines[len(art_split) + 2] == "Reginald: No history to clear."
    assert term_stdout_lines[len(art_split) + 3] == ">>> "


def test_chat_interact_slash_clear_history():
    result = runner.invoke(cli, ["chat"], input="\clear_history\n")
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[: len(art_split)] == art_split
    assert term_stdout_lines[len(art_split) + 1] == ">>> "
    assert term_stdout_lines[len(art_split) + 2] == "Reginald: No history to clear."
    assert term_stdout_lines[len(art_split) + 3] == ">>> "
