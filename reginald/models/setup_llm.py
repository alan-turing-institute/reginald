import pathlib

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
    n_gpu_layers: int | None = None,
    device: str | None = None,
) -> ResponseModel:
    # default for model
    if model is None:
        model = "hello"
    model = model.lower()
    if model not in MODELS.keys():
        raise ValueError(f"Model '{model}' not recognised.")

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

    # default for n_gpu_layers
    if n_gpu_layers is None:
        n_gpu_layers = 0

    # default for device
    if device is None:
        device = "auto"

    # set up response model
    if model == "hello":
        model = MODELS[model]
        response_model = model()
        return response_model

    model = MODELS[model]
    response_model = model(
        model_name=model_name,
        max_input_size=max_input_size,
        n_gpu_layers=n_gpu_layers,
        device=device,
        data_dir=data_dir,
        which_index=which_index,
        mode=mode,
        force_new_index=force_new_index,
    )
    return response_model
