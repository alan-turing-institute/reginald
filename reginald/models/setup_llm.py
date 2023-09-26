import logging
import pathlib
import sys

from reginald.models.models import DEFAULTS, MODELS
from reginald.models.models.base import ResponseModel


def setup_llm(
    model: str | None = None,
    model_name: str | None = None,
    mode: str | None = None,
    data_dir: str | None = None,
    which_index: str | None = None,
    force_new_index: bool | str | None = None,
    max_input_size: int | None = None,
    is_path: bool | str | None = None,
    n_gpu_layers: int | None = None,
    device: str | None = None,
) -> ResponseModel:
    """
    Set up a query or chat engine with an LLM.

    Parameters
    ----------
    model : str | None, optional
        Which type of model to use, by default None (uses "hello" model)
    model_name : str | None, optional
        Select which sub-model to use within the model requested.
        For example, if by model is "llama-index-hf", this specifies
        the Huggingface model which we would like to use, default None.
        This is ignored if using 'hello' or OpenAI model types. Otherwise,
        the defaults are set in `reginald/models/models/__init__.py`
    mode : str | None, optional
        Select which mode to use between "chat" and "query",
        by default None (uses "chat"). This is ignored if not using
        llama-index
    data_dir : str | None, optional
        Location of the data, by default None
        (uses the data directory in the root of the repo)
    which_index : str | None, optional
        Specifies the directory name for looking up/writing indices.
        Currently supports 'handbook', 'wikis', 'public', or 'all_data'.
        By default None (uses 'all_data')
    force_new_index : bool | str | None, optional
        Whether to recreate the index vector store or not, by default None
        (uses False). If this is a string, it is converted to a boolean
        using `force_new_index.lower() == "true"`.
    max_input_size : int | None, optional
        Select the maximum input size for the model, by default None
        (uses 4096). Ignored if not using "llama-index-llama-cpp" or
        "llama-index-hf" models
    is_path : bool | str | None, optional
        Whether or not model_name is used as a path to the model file,
        otherwise it should be the URL to download the model,
        by default None (uses False). If this is a string, it is
        converted to a boolean using `is_path.lower() == "true"`.
        Ignored if not using "llama-index-llama-cpp" model
    n_gpu_layers : int | None, optional
        Select the number of GPU layers to use. If -1, all layers are
        offloaded to the GPU. If 0, no layers are offloaded to the GPU,
        by default None (uses 0). Ignored if not using
        "llama-index-llama-cpp" model
    device : str | None, optional
        Select which device to use, by default None (uses "auto").
        Ignored if not using "llama-index-llama-cpp" or "llama-index-hf" models

    Returns
    -------
    ResponseModel
        Sets up query or chat engine with an LLM that has
        methods `direct_message` and `channel_mention`, which takes
        a message and user_id and returns a `MessageResponse` object
        with the response message.
    """
    # default for model
    if model is None:
        model = "hello"
    model = model.lower()
    if model not in MODELS.keys():
        logging.error(f"Model '{model}' not recognised.")
        sys.exit(1)
    logging.info(f"Setting up '{model}' model.")

    # defaulf for model_name
    if model_name is None:
        model_name = DEFAULTS[model]

    # default for mode
    if mode is None:
        mode = "chat"

    # default for data_dir
    if data_dir is None:
        # data_dir by default is the data directory in the root of the repo
        data_dir = pathlib.Path(__file__).parent.parent.parent / "data"
    data_dir = pathlib.Path(data_dir).resolve()

    # default for which_index
    if which_index is None:
        which_index = "all_data"

    # default for force_new_index
    if force_new_index is None:
        force_new_index = False
    if isinstance(force_new_index, str):
        force_new_index = force_new_index.lower() == "true"

    # default for max_input_size
    if max_input_size is None:
        max_input_size = 4096

    # default for is_path
    if is_path is None:
        is_path = False
    if isinstance(is_path, str):
        is_path = is_path.lower() == "true"

    # default for n_gpu_layers
    if n_gpu_layers is None:
        n_gpu_layers = 0

    # default for device
    if device is None:
        device = "auto"

    # Set up any model args that are required
    if model == "llama-index-llama-cpp":
        model_args = {
            "model_name": model_name,
            "is_path": is_path,
            "n_gpu_layers": n_gpu_layers,
            "max_input_size": max_input_size,
        }
    elif model == "llama-index-hf":
        model_args = {
            "model_name": model_name,
            "device": device,
            "max_input_size": max_input_size,
        }
    elif model in ["llama-index-gpt-azure", "chat-completion-azure"]:
        model_args = {
            "model_name": model_name,
        }
    else:
        model_args = {}

    logging.info(f"Model args are: {model_args}.")
    # set up response model
    if model == "hello":
        model = MODELS[model]
        response_model = model()
    else:
        model = MODELS[model]
        response_model = model(
            model_name=model_name,
            max_input_size=max_input_size,
            is_path=is_path,
            n_gpu_layers=n_gpu_layers,
            device=device,
            data_dir=data_dir,
            which_index=which_index,
            force_new_index=force_new_index,
            mode=mode,
            **model_args,
        )

    return response_model
