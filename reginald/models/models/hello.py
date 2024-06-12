from typing import Any

from reginald.models.models.base import MessageResponse, ResponseModel
from reginald.utils import stream_progress_wrapper


class Hello(ResponseModel):
    def __init__(self, *args: Any, **kwargs: Any):
        """
        Basic response model that has set response to
        direct messagesa and channel mentions.
        """
        super().__init__(*args, emoji="wave", **kwargs)

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        return MessageResponse("Let's discuss this in a channel!")

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        return MessageResponse(f"Hello <@{user_id}>")

    def stream_message(self, message: str, user_id: str) -> None:
        # print("\nReginald: ", end="")
        token_list: tuple[str, ...] = ("Hello", "!", " How", " are", " you", "?")
        for token in stream_progress_wrapper(token_list):
            print(token, end="")
