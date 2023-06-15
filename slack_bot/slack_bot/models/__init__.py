from .base import ResponseModel
from .hello import Hello
from .llama import LlamaDistilGPT2, LlamaGPT35TurboPersonal, LlamaGPT35TurboAzure
from .openai_azure import OpenAIAzure
from .openai_personal import OpenAIPersonal

MODELS = {
    "hello": Hello,
    "llama-distilgpt2": LlamaDistilGPT2,
    "llama-gpt-3.5-turbo-azure": LlamaGPT35TurboAzure,
    "llama-gpt-3.5-turbo-personal": LlamaGPT35TurboPersonal,
    "openai-azure": OpenAIAzure,
    "openai-personal": OpenAIPersonal,
}

__all__ = ["MODELS", "ResponseModel"]
