import logging
from typing import Any, Callable

from llama_index.core import set_global_tokenizer
from llama_index.llms.huggingface import HuggingFaceLLM
from transformers import AutoTokenizer

from reginald.models.llama_index.base import LlamaIndex


class LlamaIndexHF(LlamaIndex):
    def __init__(
        self,
        model_name: str = "google/gemma-2b-it",
        device: str = "auto",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        `LlamaIndexHF` is a subclass of `LlamaIndex` that uses HuggingFace's
        `transformers` library to implement the LLM.

        Parameters
        ----------
        model_name : str, optional
            Model name from Huggingface's model hub,
            by default "google/gemma-2b-it".
        device : str, optional
            Device map to use for the LLM, by default "auto".
        """
        self.device = device
        super().__init__(*args, model_name=model_name, **kwargs)

    def _prep_llm(self) -> HuggingFaceLLM:
        logging.info(
            f"Setting up Huggingface LLM (model {self.model_name}) on device {self.device}"
        )
        logging.info(
            f"HF-args: (context_window: {self.max_input_size}, num_output: {self.num_output})"
        )

        return HuggingFaceLLM(
            context_window=self.max_input_size,
            max_new_tokens=self.num_output,
            generate_kwargs={"temperature": 0.1, "do_sample": False},
            tokenizer_name=self.model_name,
            model_name=self.model_name,
            device_map=self.device or "auto",
        )

    def _prep_tokenizer(self) -> Callable[[str], int]:
        logging.info(f"Setting up Huggingface tokenizer for model {self.model_name}")
        tokenizer = AutoTokenizer.from_pretrained(self.model_name).encode
        set_global_tokenizer(tokenizer)
        return tokenizer
