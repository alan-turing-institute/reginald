import time

from .base import MessageResponse, ResponseModel


class Hello(ResponseModel):
    def __init__(self):
        super().__init__(emoji="wave")

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        time.sleep(5)
        return MessageResponse("Let's discuss this in a channel!")

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        time.sleep(5)
        return MessageResponse(f"Hello <@{user_id}>")
