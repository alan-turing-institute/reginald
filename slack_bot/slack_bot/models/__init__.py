from .base import ResponseModel
from .hello import Hello
from .llama import LlamaDistilGPT2, LlamaGPT35Turbo
from .openai_azure import OpenAIAzure
from .openai_personal import OpenAIPersonal

MODELS = {
    "hello": Hello,
    "llama-distilgpt2": LlamaDistilGPT2,
    "llama-gpt-3.5-turbo": LlamaGPT35Turbo,
    "openai_azure": OpenAIAzure,
    "openai_personal": OpenAIPersonal,
}

__all__ = ["MODELS", "ResponseModel"]
