# Standard library imports
import os

# Third-party imports
import openai

# Local imports
from .base import MessageResponse, ResponseModel


class OpenAI(ResponseModel):
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]
        )
        text = response["choices"][0]["message"]["content"]
        return MessageResponse(text, None)

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]
        )
        text = response["choices"][0]["message"]["content"]
        return MessageResponse(text, None)
