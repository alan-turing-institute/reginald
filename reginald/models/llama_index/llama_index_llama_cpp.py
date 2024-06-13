import logging
from typing import Any, Callable

from llama_index.core import set_global_tokenizer
from llama_index.llms.llama_cpp import LlamaCPP
from tiktoken import encoding_for_model

from reginald.models.llama_index.base import LlamaIndex
from reginald.models.llama_index.llama_cpp_template import (
    completion_to_prompt,
    messages_to_prompt,
)


class LlamaIndexLlamaCPP(LlamaIndex):
    def __init__(
        self,
        model_name: str,
        is_path: bool,
        n_gpu_layers: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        `LlamaIndexLlamaCPP` is a subclass of `LlamaIndex` that uses
        llama-cpp to implement the LLM.

        Parameters
        ----------
        model_name : str
            Either the path to the model or the URL to download the model from
        is_path : bool, optional
            If True, model_name is used as a path to the model file,
            otherwise it should be the URL to download the model
        n_gpu_layers : int, optional
            Number of layers to offload to GPU.
            If -1, all layers are offloaded, by default 0
        """
        self.is_path = is_path
        self.n_gpu_layers = n_gpu_layers
        super().__init__(*args, model_name=model_name, **kwargs)

    def _prep_llm(self) -> LlamaCPP:
        logging.info(
            f"Setting up LlamaCPP LLM (model {self.model_name}) on {self.n_gpu_layers} GPU layers"
        )
        logging.info(
            f"LlamaCPP-args: (context_window: {self.max_input_size}, num_output: {self.num_output})"
        )

        return LlamaCPP(
            model_url=self.model_name if not self.is_path else None,
            model_path=self.model_name if self.is_path else None,
            temperature=0.1,
            max_new_tokens=self.num_output,
            context_window=self.max_input_size,
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            model_kwargs={"n_gpu_layers": self.n_gpu_layers},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=True,
        )

    def _prep_tokenizer(self) -> Callable[[str], int]:
        # NOTE: this should depend on the model used, but hard coding tiktoken for now
        logging.info("Setting up tiktoken gpt-4 tokenizer")
        tokenizer = encoding_for_model("gpt-4").encode
        set_global_tokenizer(tokenizer)
        return tokenizer
