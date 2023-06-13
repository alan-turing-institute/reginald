from .base import MessageResponse, ResponseModel


class Hello(ResponseModel):
    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        return MessageResponse(None, "tada")

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        return MessageResponse(f"Hello <@{user_id}>", "+1")
