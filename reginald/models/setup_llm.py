from reginald.models.models import MODELS


def setup_llm(**kwargs):
    if kwargs["model"] not in MODELS:
        raise ValueError(f"Model '{kwargs['model']} not recognised.")

    if kwargs["model"] == "hello":
        model = MODELS[kwargs["model"]]
        response_model = model()
        return response_model

    if kwargs["model"] == "llama-index-llama-cpp":
        model_args = {
            "model_name": kwargs["model_name"],
            "n_gpu_layers": kwargs["n_gpu_layers"],
            "max_input_size": kwargs["max_input_size"],
        }

    elif kwargs["model"] == "llama-index-hf":
        model_args = {
            "model_name": kwargs["model_name"],
            "device": kwargs["device"],
            "max_input_size": kwargs["max_input_size"],
        }

    elif kwargs["model"] in ["chat-completion-azure", "llama-index-gpt-azure"]:
        model_args = {
            "deployment_name": kwargs["model_name"],
        }

    model = MODELS[kwargs["model"]]
    response_model = model(
        force_new_index=kwargs["force_new_index"],
        data_dir=kwargs["data_dir"],
        which_index=kwargs["which_index"],
        mode=kwargs["mode"],
        **model_args,
    )
    return response_model
