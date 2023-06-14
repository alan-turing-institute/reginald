# Standard library imports
import os

# Third-party imports
import openai

# Local imports
from .base import MessageResponse, ResponseModel


class OpenAIAzure(ResponseModel):
    def __init__(self) -> None:
        self.api_base = os.getenv("OPENAI_API_BASE")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_type = "azure"
        self.api_version = "2023-03-15-preview"
        self.engine = "reginald-gpt35",

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        openai.api_base = self.api_base
        openai.api_type = self.api_type
        openai.api_version = self.api_version
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            engine=self.engine,
            frequency_penalty=0,
            max_tokens=110,
            presence_penalty=0,
            prompt=message,
            stop=None,
            temperature=1,
            top_p=1,
        )
        text = response["choices"][0]["message"]["content"]
        return MessageResponse(text, None)

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        openai.api_base = self.api_base
        openai.api_type = self.api_type
        openai.api_version = self.api_version
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            engine=self.engine,
            frequency_penalty=0,
            max_tokens=110,
            presence_penalty=0,
            prompt=message,
            stop=None,
            temperature=1,
            top_p=1,
        )
        text = response["choices"][0]["message"]["content"]
        return MessageResponse(text, None)
