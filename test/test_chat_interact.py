import builtins
from unittest import mock

import pytest
from typer.testing import CliRunner

from reginald.cli import cli
from reginald.models.models.hello import Hello
from reginald.run import chat_interact

runner = CliRunner()


def test_chat_cli():
    """Test sending an input `str` via `cli` and then exiting."""
    result = runner.invoke(cli, ["chat"], input="What's up dock?\nexit\n")
    term_stdout_lines: list[str] = result.stdout.split("\n")
    assert term_stdout_lines[0] == ">>> Reginald: Let's discuss this in a channel!"
    assert term_stdout_lines[1] == ">>> "


def test_chat_interact_exit():
    with mock.patch.object(builtins, "input", lambda _: "exit"):
        interaction = chat_interact(model="hello")
    assert isinstance(interaction, Hello)
