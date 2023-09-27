import logging
import os
from typing import Any

import openai

from reginald.models.models.base import MessageResponse, ResponseModel


class ChatCompletionBase(ResponseModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(emoji="books")


class ChatCompletionAzure(ChatCompletionBase):
    def __init__(
        self, model_name: str = "reginald-curie", *args: Any, **kwargs: Any
    ) -> None:
        logging.info(f"Setting up AzureOpenAI LLM (model {model_name})")
        super().__init__(*args, **kwargs)
        self.api_base = os.getenv("OPENAI_AZURE_API_BASE")
        self.api_key = os.getenv("OPENAI_AZURE_API_KEY")
        self.api_type = "azure"
        self.api_version = "2023-03-15-preview"
        self.best_of = 1
        self.engine = model_name  # the deployment name
        self.frequency_penalty = 0
        self.max_tokens = 100
        self.presence_penalty = 0
        self.temperature = 0.2
        self.top_p = 0.95

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        openai.api_base = self.api_base
        openai.api_type = self.api_type
        openai.api_version = self.api_version
        openai.api_key = self.api_key
        response = openai.Completion.create(
            best_of=self.best_of,
            engine=self.engine,
            frequency_penalty=self.frequency_penalty,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty,
            prompt=message,
            stop=None,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        return MessageResponse(response["choices"][0]["text"])

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        openai.api_base = self.api_base
        openai.api_type = self.api_type
        openai.api_version = self.api_version
        openai.api_key = self.api_key
        response = openai.Completion.create(
            best_of=self.best_of,
            engine=self.engine,
            frequency_penalty=self.frequency_penalty,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty,
            prompt=message,
            stop=None,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        return MessageResponse(response["choices"][0]["text"])


class ChatCompletionOpenAI(ChatCompletionBase):
    def __init__(
        self, model_name: str = "gpt-3.5-turbo", *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model_name, messages=[{"role": "user", "content": message}]
        )
        return MessageResponse(response["choices"][0]["message"]["content"])

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model_name, messages=[{"role": "user", "content": message}]
        )
        return MessageResponse(response["choices"][0]["message"]["content"])
