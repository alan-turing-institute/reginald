class ModelMapper:
    @staticmethod
    def available_models():
        return [
            "chat-completion-azure",
            "chat-completion-openai",
            "hello",
            "llama-index-ollama",
            "llama-index-llama-cpp",
            "llama-index-hf",
            "llama-index-gpt-azure",
            "llama-index-gpt-openai",
        ]

    @staticmethod
    def get_model(model_name: str):
        match model_name:
            case "chat-completion-azure":
                from reginald.models.simple.chat_completion import ChatCompletionAzure

                return ChatCompletionAzure
            case "chat-completion-openai":
                from reginald.models.simple.chat_completion import ChatCompletionOpenAI

                return ChatCompletionOpenAI
            case "hello":
                from reginald.models.simple.hello import Hello

                return Hello
            case "llama-index-ollama":
                from reginald.models.llama_index.llama_index_ollama import (
                    LlamaIndexOllama,
                )

                return LlamaIndexOllama
            case "llama-index-llama-cpp":
                from reginald.models.llama_index.llama_index_llama_cpp import (
                    LlamaIndexLlamaCPP,
                )

                return LlamaIndexLlamaCPP
            case "llama-index-hf":
                from reginald.models.llama_index.llama_index_hf import LlamaIndexHF

                return LlamaIndexHF
            case "llama-index-gpt-azure":
                from reginald.models.llama_index.llama_index_azure_openai import (
                    LlamaIndexGPTAzure,
                )

                return LlamaIndexGPTAzure
            case "llama-index-gpt-openai":
                from reginald.models.llama_index.llama_index_openai import (
                    LlamaIndexGPTOpenAI,
                )

                return LlamaIndexGPTOpenAI
            case _:
                raise ValueError(
                    f"Model {model_name} not found. Available models: {ModelMapper.available_models()}"
                )


DEFAULTS = {
    "chat-completion-azure": "reginald-gpt4",
    "chat-completion-openai": "gpt-3.5-turbo",
    "hello": None,
    "llama-index-ollama": "llama3",
    "llama-index-llama-cpp": "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q6_K.gguf",
    "llama-index-hf": "microsoft/phi-1_5",
    "llama-index-gpt-azure": "reginald-gpt4",
    "llama-index-gpt-openai": "gpt-3.5-turbo",
}

__all__ = ["MODELS", "DEFAULTS"]
