import pytest

from reginald.models.models.hello import Hello
from reginald.run import chat_interact


def test_chat_interact(monkeypatch):
    user_inputs = iter(["What's up?", "exit"])
    interaction = chat_interact(model="hello")

    monkeypatch.setattr("builtins.input", lambda name: next(user_inputs))
    assert isinstance(interaction, Hello)

    # captured = capsys.readouterr()
    # assert "Reginald: Let's discuss this in a channel!" in captured.out


def test_chat_interact_exit(monkeypatch):
    inputs = []
    interaction = chat_interact(model="hello")

    monkeypatch.setattr("builtins.input", lambda name: next(inputs))

    assert isinstance(interaction, Hello)
