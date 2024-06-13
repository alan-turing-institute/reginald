import logging
from typing import Any

from llama_index.core import set_global_tokenizer
from llama_index.llms.openai import OpenAI

from reginald.models.llama_index.base import LlamaIndex
from reginald.utils import get_env_var


class LlamaIndexGPTOpenAI(LlamaIndex):
    def __init__(
        self, model_name: str = "gpt-3.5-turbo", *args: Any, **kwargs: Any
    ) -> None:
        """
        `LlamaIndexGPTOpenAI` is a subclass of `LlamaIndex` that uses OpenAI's
        API to implement the LLM.

        Must have `OPENAI_API_KEY` set as an environment variable.

        Parameters
        ----------
        model_name : str, optional
            The model to use from the OpenAI API, by default "gpt-3.5-turbo"
        """
        openai_api_key = get_env_var("OPENAI_API_KEY")
        if openai_api_key is None:
            raise ValueError("You must set OPENAI_API_KEY for OpenAI.")

        self.model_name = model_name
        self.openai_api_key = openai_api_key
        self.temperature = 0.7
        super().__init__(*args, model_name=self.model_name, **kwargs)

    def _prep_llm(self) -> OpenAI:
        logging.info(f"Setting up OpenAI LLM (model {self.model_name})")
        return OpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.num_output,
            api_key=self.openai_api_key,
        )

    def _prep_tokenizer(self) -> None:
        import tiktoken

        logging.info(f"Setting up tiktoken tokenizer for model {self.model_name}")
        tokenizer = tiktoken.encoding_for_model(self.model_name).encode
        set_global_tokenizer(tokenizer)
        return tokenizer
