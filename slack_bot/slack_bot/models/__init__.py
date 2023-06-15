from .base import ResponseModel
from .chat_completion import ChatCompletionAzure, ChatCompletionOpenAI
from .hello import Hello
from .llama import LlamaDistilGPT2, LlamaGPT35TurboAzure, LlamaGPT35TurboOpenAI

# Please ensure that any models needing OPENAI_API_KEY are named *openai*
# Please ensure that any models needing OPENAI_AZURE_API_BASE and OPENAI_AZURE_API_KEY are named *azure*
MODELS = {
    "chat-completion-azure": ChatCompletionAzure,
    "chat-completion-openai": ChatCompletionOpenAI,
    "hello": Hello,
    "llama-distilgpt2": LlamaDistilGPT2,
    "llama-gpt-3.5-turbo-azure": LlamaGPT35TurboAzure,
    "llama-gpt-3.5-turbo-openai": LlamaGPT35TurboOpenAI,
}

__all__ = ["MODELS", "ResponseModel"]
