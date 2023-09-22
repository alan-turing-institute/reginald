from reginald.models.models.base import MessageResponse, ResponseModel


class Hello(ResponseModel):
    def __init__(self):
        super().__init__(emoji="wave")

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        return MessageResponse("Let's discuss this in a channel!")

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        return MessageResponse(f"Hello <@{user_id}>")
