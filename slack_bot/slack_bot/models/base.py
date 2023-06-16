# Standard library imports
from abc import ABC
from typing import Any, Optional


class MessageResponse:
    def __init__(self, message: Optional[str], emoji: Optional[str]) -> None:
        self.message = message
        self.emoji = emoji


class ResponseModel(ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        """When the strategy receives a message it should return a MessageResponse where both are optional"""
        raise NotImplementedError

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        """When the strategy receives a message it should return a MessageResponse where both are optional"""
        raise NotImplementedError
