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
        self.frequency_penalty = 0
        self.max_tokens = 110
        self.presence_penalty = 0
        self.temperature = 1
        self.top_p = 1

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        openai.api_base = self.api_base
        openai.api_type = self.api_type
        openai.api_version = self.api_version
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            engine=self.engine,
            frequency_penalty=self.frequency_penalty,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty,
            prompt=message,
            stop=None,
            temperature=self.temperature,
            top_p=self.top_p,
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
            frequency_penalty=self.frequency_penalty,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty,
            prompt=message,
            stop=None,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        text = response["choices"][0]["message"]["content"]
        return MessageResponse(text, None)
