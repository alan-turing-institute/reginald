from .base import ResponseModel
from .chat_completion import ChatCompletionAzure, ChatCompletionOpenAI
from .hello import Hello
from .llama_index import (
    LlamaIndexGPTAzure,
    LlamaIndexGPTOpenAI,
    LlamaIndexHF,
    LlamaIndexLlamaCPP,
)

# Please ensure that any models needing OPENAI_API_KEY are named *openai*
# Please ensure that any models needing OPENAI_AZURE_API_BASE and OPENAI_AZURE_API_KEY are named *azure*
MODELS = {
    "chat-completion-azure": ChatCompletionAzure,
    "chat-completion-openai": ChatCompletionOpenAI,
    "hello": Hello,
    "llama-index-llama-cpp": LlamaIndexLlamaCPP,
    "llama-index-hf": LlamaIndexHF,
    "llama-index-gpt-azure": LlamaIndexGPTAzure,
    "llama-index-gpt-openai": LlamaIndexGPTOpenAI,
}

__all__ = ["MODELS", "ResponseModel"]
