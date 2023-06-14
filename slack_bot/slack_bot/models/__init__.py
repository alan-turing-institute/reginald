from .base import ResponseModel
from .hello import Hello
from .llama import LlamaDistilGPT2, LlamaGPT35Turbo
from .openai import OpenAI
from .openai_azure import OpenAIAzure

MODELS = {
    "hello": Hello,
    "llama-distilgpt2": LlamaDistilGPT2,
    "llama-gpt-3.5-turbo": LlamaGPT35Turbo,
    "openai": OpenAI,
    "openai_azure": OpenAIAzure,
}

__all__ = ["MODELS", "ResponseModel"]
