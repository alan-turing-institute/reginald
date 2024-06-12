# Standard library imports
from abc import ABC
from typing import Any, Optional


class MessageResponse:
    def __init__(self, message: Optional[str]) -> None:
        """
        Class for holding the response message.

        Parameters
        ----------
        message : Optional[str]
            Message to send back to Slack
        """
        self.message = message


class ResponseModel(ABC):
    def __init__(self, emoji: Optional[str], *args: Any, **kwargs: Any):
        """
        When the strategy receives a message it should
        return a `MessageResponse` where both are optional.

        Parameters
        ----------
        emoji : Optional[str]
            Emoji to use for the bot's response
        """
        self.emoji = emoji
        self.mode = "NA"

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        raise NotImplementedError

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        raise NotImplementedError

    def stream_message(self, message: str, user_id: str) -> None:
        raise NotImplementedError
