from .base import ResponseModel
from .hello import Hello
from .llama import LlamaDistilGPT2, LlamaGPT35TurboOpenAI, LlamaGPT35TurboAzure
from .chat_completion import ChatCompletionAzure, ChatCompletionOpenAI

MODELS = {
    "hello": Hello,
    "llama-distilgpt2": LlamaDistilGPT2,
    "llama-gpt-3.5-turbo-azure": LlamaGPT35TurboAzure,
    "llama-gpt-3.5-turbo-openai": LlamaGPT35TurboOpenAI,
    "chat-completion-azure": ChatCompletionAzure,
    "chat-completion-openai": ChatCompletionOpenAI,
}

__all__ = ["MODELS", "ResponseModel"]
