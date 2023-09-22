import os
import pathlib

from reginald.models.models import MODELS

DEFAULT_LLAMA_CPP_GGUF_MODEL = (
    "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve"
    "/main/llama-2-13b-chat.Q6_K.gguf"
)
DEFAULT_HF_MODEL = "StabilityAI/stablelm-tuned-alpha-3b"
DEFAULT_LLAMA_INDEX_AZURE_DEPLOYMENT = "reginald-gpt35-turbo"
DEFAULT_CHAT_COMPLETION_AZURE_DEPLOYMENT = "reginald-curie"


def setup_llm():
    # choose model
    model = os.environ.get("REGINALD_MODEL") or "hello"
    model = model.lower()

    # set up variables
    mode = os.environ.get("LLAMA_INDEX_MODE") or "chat"
    max_input_size = os.environ.get("LLAMA_INDEX_MAX_INPUT_SIZE") or 4096
    ngl = os.environ.get("LLAMA_INDEX_N_GPU_LAYERS") or 0
    device = os.environ.get("LLAMA_INDEX_DEVICE") or "auto"
    data_dir = (
        pathlib.Path(os.environ.get("LLAMA_INDEX_DATA_DIR")).resolve()
        or (pathlib.Path(__file__).parent.parent / "data").resolve()
    )
    which_index = os.environ.get("LLAMA_INDEX_WHICH_INDEX") or "all_data"
    force_new_index = os.environ.get("LLAMA_INDEX_FORCE_NEW_INDEX")
    force_new_index = (
        (force_new_index.lower() == "true") if force_new_index else False
    )  # no command line args, behaviour now is do env variable or set False

    if model == "hello":
        model = MODELS[model]
        response_model = model()
        return response_model

    if model == "llama-index-llama-cpp":
        # try to obtain model name from env var
        # or use default if none provided
        model_name = (
            os.environ.get("LLAMA_INDEX_MODEL_NAME") or DEFAULT_LLAMA_CPP_GGUF_MODEL
        )

        model_args = {
            "model_name": model_name,
            "n_gpu_layers": ngl,
            "max_input_size": max_input_size,
        }

    elif model == "llama-index-hf":
        # try to obtain model name from env var
        # or use default if none provided
        model_name = os.environ.get("LLAMA_INDEX_MODEL_NAME") or DEFAULT_HF_MODEL

        model_args = {
            "model_name": model_name,
            "device": device,
            "max_input_size": max_input_size,
        }

    elif model in ["chat-completion-azure", "llama-index-gpt-azure"]:
        # try to obtain model name from env var
        # or use default if none provided
        if model == "chat-completion-azure":
            model_name = (
                os.environ.get("LLAMA_INDEX_MODEL_NAME")
                or DEFAULT_CHAT_COMPLETION_AZURE_DEPLOYMENT
            )
        elif model == "llama-index-gpt-azure":
            model_name = (
                os.environ.get("LLAMA_INDEX_MODEL_NAME")
                or DEFAULT_LLAMA_INDEX_AZURE_DEPLOYMENT
            )

        model_args = {
            "deployment_name": model_name,
        }

    else:
        raise ValueError(f"Model '{model}' not recognised.")

    model = MODELS[model]
    response_model = model(
        force_new_index=force_new_index,
        data_dir=data_dir,
        which_index=which_index,
        mode=mode,
        **model_args,
    )
    return response_model
