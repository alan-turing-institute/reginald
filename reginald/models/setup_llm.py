import logging
import pathlib
import sys

from reginald.models.models import DEFAULTS, MODELS
from reginald.models.models.base import ResponseModel

DEFAULT_ARGS = {
    "model": "hello",
    "mode": "chat",
    "data_dir": pathlib.Path(__file__).parent.parent.parent / "data",
    "which_index": "all_data",
    "force_new_index": False,
    "max_input_size": 4096,
    "k": 3,
    "chunk_overlap_ratio": 0.1,
    "num_output": 512,
    "is_path": False,
    "n_gpu_layers": 0,
    "device": "auto",
}


def setup_llm(
    model: str | None = None,
    model_name: str | None = None,
    mode: str | None = None,
    data_dir: str | None = None,
    which_index: str | None = None,
    force_new_index: bool | str | None = None,
    max_input_size: int | str | None = None,
    k: int | str | None = None,
    chunk_size: int | str | None = None,
    chunk_overlap_ratio: float | str | None = None,
    num_output: int | str | None = None,
    is_path: bool | str | None = None,
    n_gpu_layers: int | str | None = None,
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
        This is ignored if using 'hello' model.
        Otherwise, the defaults are set in `reginald/models/models/__init__.py`
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
    max_input_size : int | str | None, optional
        Select the maximum input size for the model, by default None
        (uses 4096). Ignored if not using "llama-index-llama-cpp" or
        "llama-index-hf" models, If this is a string, it is converted
        to an integer
    k : int | str | None, optional
        `similarity_top_k` to use in chat or query engine,
        by default None (uses 3). If this is a string, it is converted
        to an integer
    chunk_size : int | str | None, optional
        Maximum size of chunks to use, by default None.
        If None, this is computed as `ceil(max_input_size / k)`.
        If this is a string, it is converted to an integer
    chunk_overlap_ratio : float | str | None, optional
        Chunk overlap as a ratio of chunk size, by default None (uses 0.1).
        If this is a string, it is converted to a float
    num_output : int | str | None, optional
        Number of outputs for the LLM, by default None (uses 512).
        If this is a string, it is converted to an integer
    is_path : bool | str | None, optional
        Whether or not model_name is used as a path to the model file,
        otherwise it should be the URL to download the model,
        by default None (uses False). If this is a string, it is
        converted to a boolean using `is_path.lower() == "true"`.
        Ignored if not using "llama-index-llama-cpp" model
    n_gpu_layers : int | str | None, optional
        Select the number of GPU layers to use. If -1, all layers are
        offloaded to the GPU. If 0, no layers are offloaded to the GPU,
        by default None (uses 0). Ignored if not using
        "llama-index-llama-cpp" model. If this is a string, it is
        converted to an integer
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
        model = DEFAULT_ARGS["model"]
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
        mode = DEFAULT_ARGS["mode"]

    # default for data_dir
    if data_dir is None:
        # data_dir by default is the data directory in the root of the repo
        data_dir = DEFAULT_ARGS["data_dir"]
    data_dir = pathlib.Path(data_dir).resolve()

    # default for which_index
    if which_index is None:
        which_index = DEFAULT_ARGS["which_index"]

    # default for force_new_index
    if force_new_index is None:
        force_new_index = DEFAULT_ARGS["force_new_index"]
    if isinstance(force_new_index, str):
        force_new_index = force_new_index.lower() == "true"

    # default for max_input_size
    if max_input_size is None:
        max_input_size = DEFAULT_ARGS["max_input_size"]
    if isinstance(max_input_size, str):
        max_input_size = int(max_input_size)

    # default for k
    if k is None:
        k = DEFAULT_ARGS["k"]
    if isinstance(k, str):
        k = int(k)

    # convert chunk_size if provided as str
    # default is computed later using values of max_input_size and k
    if isinstance(chunk_size, str):
        chunk_size = int(chunk_size)

    # default for chunk_overlap_ratio
    if chunk_overlap_ratio is None:
        chunk_overlap_ratio = DEFAULT_ARGS["chunk_overlap_ratio"]
    if isinstance(chunk_overlap_ratio, str):
        chunk_overlap_ratio = float(chunk_overlap_ratio)

    # default for num_output
    if num_output is None:
        num_output = DEFAULT_ARGS["num_output"]
    if isinstance(num_output, str):
        num_output = int(num_output)

    # default for is_path
    if is_path is None:
        is_path = DEFAULT_ARGS["is_path"]
    if isinstance(is_path, str):
        is_path = is_path.lower() == "true"

    # default for n_gpu_layers
    if n_gpu_layers is None:
        n_gpu_layers = DEFAULT_ARGS["n_gpu_layers"]
    if isinstance(n_gpu_layers, str):
        n_gpu_layers = int(n_gpu_layers)

    # default for device
    if device is None:
        device = DEFAULT_ARGS["device"]

    # set up response model
    model = MODELS[model]
    response_model = model(
        model_name=model_name,
        max_input_size=max_input_size,
        data_dir=data_dir,
        which_index=which_index,
        mode=mode,
        k=k,
        chunk_size=chunk_size,
        chunk_overlap_ratio=chunk_overlap_ratio,
        num_output=num_output,
        force_new_index=force_new_index,
        is_path=is_path,
        n_gpu_layers=n_gpu_layers,
        device=device,
    )

    return response_model
