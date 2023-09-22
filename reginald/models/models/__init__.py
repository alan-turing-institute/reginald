from reginald.models.models.chat_completion import (
    ChatCompletionAzure,
    ChatCompletionOpenAI,
)
from reginald.models.models.hello import Hello
from reginald.models.models.llama_index import (
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

DEFAULTS = {
    "chat-completion-azure": "reginald-curie",
    "llama-index-llama-cpp": "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q6_K.gguf",
    "llama-index-hf": "StabilityAI/stablelm-tuned-alpha-3b",
    "llama-index-gpt-azure": "reginald-gpt35-turbo",
}

__all__ = ["MODELS", "DEFAULTS"]
