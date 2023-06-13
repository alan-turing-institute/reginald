from .base import BaseStrategy, MessageResponse


class Hello(BaseStrategy):
    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        """When the strategy receives a message it should return a MessageResponse"""
        return MessageResponse(None, "eyes")


    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        """When the strategy receives a message it should return a MessageResponse"""
        return MessageResponse(f"Hello <@{user_id}>", "+1")
