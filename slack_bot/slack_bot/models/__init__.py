from .base import ResponseModel
from .chat_completion import ChatCompletionAzure, ChatCompletionOpenAI
from .hello import Hello
from .llama_index import LlamaIndexGPTAzure, LlamaIndexGPTOpenAI, LlamaIndexHF

# Please ensure that any models needing OPENAI_API_KEY are named *openai*
# Please ensure that any models needing OPENAI_AZURE_API_BASE and OPENAI_AZURE_API_KEY are named *azure*
MODELS = {
    "chat-completion-azure": ChatCompletionAzure,
    "chat-completion-openai": ChatCompletionOpenAI,
    "hello": Hello,
    "llama-index-hf": LlamaIndexHF,
    "llama-index-gpt-3.5-turbo-azure": LlamaIndexGPTAzure,
    "llama-index-gpt-3.5-turbo-openai": LlamaIndexGPTOpenAI,
}

__all__ = ["MODELS", "ResponseModel"]
