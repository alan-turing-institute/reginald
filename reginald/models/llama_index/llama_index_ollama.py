import logging
from typing import Any, Callable

from llama_index.core import set_global_tokenizer
from llama_index.llms.ollama import Ollama
from tiktoken import encoding_for_model

from reginald.models.llama_index.base import LlamaIndex
from reginald.utils import get_env_var


class LlamaIndexOllama(LlamaIndex):
    def __init__(
        self,
        model_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        `LlamaIndexOllama` is a subclass of `LlamaIndex` that uses
        ollama to run inference on the LLM.

        Parameters
        ----------
        model_name : str
            The Ollama model to use
        """
        ollama_api_endpoint = get_env_var("OLLAMA_API_ENDPOINT")
        if ollama_api_endpoint is None:
            raise ValueError("You must set OLLAMA_API_ENDPOINT for Ollama.")
        self.ollama_api_endpoint = ollama_api_endpoint
        super().__init__(*args, model_name=model_name, **kwargs)

    def _prep_llm(self) -> Ollama:
        logging.info(f"Setting up Ollama (model {self.model_name})")
        return Ollama(
            base_url=self.ollama_api_endpoint,
            model=self.model_name,
            request_timeout=60,
        )

    def _prep_tokenizer(self) -> Callable[[str], int]:
        # NOTE: this should depend on the model used, but hard coding tiktoken for now
        logging.info("Setting up tiktoken gpt-4 tokenizer")
        tokenizer = encoding_for_model("gpt-4").encode
        set_global_tokenizer(tokenizer)
        return tokenizer
