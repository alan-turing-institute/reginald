import pathlib
from typing import Annotated, Optional

import typer

from reginald.models.setup_llm import DEFAULT_ARGS
from reginald.run import EMOJI_DEFAULT, main

API_URL_PROPMPT = "No API URL was provided and REGINALD_API_URL not set. Please provide an API URL for the Reginald app"

cli = typer.Typer()

# TODO: before, using get_env_var would print out whenever it's being called and an env var is attempted to be loaded
# (only when necessary, i.e. not provided), is it possible to tell the user that an env var is going to be used?
# TODO: create config class
# TODO: add help


@cli.command()
def run_all(
    model: Annotated[
        str,
        typer.Option(
            envvar="REGINALD_MODEL",
            help="Select which type of model to use. Default is 'hello'.",
        ),
    ] = DEFAULT_ARGS["model"],
    model_name: Annotated[
        Optional[str], typer.Option(envvar="REGINALD_MODEL_NAME")
    ] = None,
    mode: Annotated[str, typer.Option(envvar="LLAMA_INDEX_MODE")] = DEFAULT_ARGS[
        "mode"
    ],
    data_dir: Annotated[
        pathlib.Path, typer.Option(envvar="LLAMA_INDEX_DATA_DIR")
    ] = DEFAULT_ARGS["data_dir"],
    which_index: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_WHICH_INDEX")
    ] = DEFAULT_ARGS["which_index"],
    force_new_index: Annotated[
        bool, typer.Option(envvar="LLAMA_INDEX_FORCE_NEW_INDEX")
    ] = DEFAULT_ARGS["force_new_index"],
    max_input_size: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_MAX_INPUT_SIZE")
    ] = DEFAULT_ARGS["max_input_size"],
    k: Annotated[int, typer.Option(envvar="LLAMA_INDEX_K")] = DEFAULT_ARGS["k"],
    chunk_size: Annotated[
        Optional[int], typer.Option(envvar="LLAMA_INDEX_CHUNK_SIZE")
    ] = DEFAULT_ARGS.get("chunk_size"),
    chunk_overlap_ratio: Annotated[
        float, typer.Option(envvar="LLAMA_INDEX_CHUNK_OVERLAP_RATIO")
    ] = DEFAULT_ARGS["chunk_overlap_ratio"],
    num_output: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_NUM_OUTPUT")
    ] = DEFAULT_ARGS["num_output"],
    is_path: Annotated[bool, typer.Option(envvar="LLAMA_INDEX_IS_PATH")] = DEFAULT_ARGS[
        "is_path"
    ],
    n_gpu_layers: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_N_GPU_LAYERS")
    ] = DEFAULT_ARGS["n_gpu_layers"],
    device: Annotated[str, typer.Option(envvar="LLAMA_INDEX_DEVICE")] = DEFAULT_ARGS[
        "device"
    ],
) -> None:
    main(
        cli="run_all",
        model=model,
        model_name=model_name,
        mode=mode,
        data_dir=data_dir,
        which_index=which_index,
        force_new_index=force_new_index,
        max_input_size=max_input_size,
        k=k,
        chunk_size=chunk_size,
        chunk_overlap_ratio=chunk_overlap_ratio,
        num_output=num_output,
        is_path=is_path,
        n_gpu_layers=n_gpu_layers,
        device=device,
    )


@cli.command()
def bot(
    api_url: Annotated[
        str, typer.Option(prompt=API_URL_PROPMPT, envvar="REGINALD_API_URL")
    ],
    emoji: Annotated[str, typer.Option(envvar="REGINALD_EMOJI")] = EMOJI_DEFAULT,
) -> None:
    main(
        cli="bot",
        api_url=api_url,
        emoji=emoji,
    )


@cli.command()
def app(
    model: Annotated[str, typer.Option(envvar="REGINALD_MODEL")] = DEFAULT_ARGS[
        "model"
    ],
    model_name: Annotated[
        Optional[str], typer.Option(envvar="REGINALD_MODEL_NAME")
    ] = None,
    mode: Annotated[str, typer.Option(envvar="LLAMA_INDEX_MODE")] = DEFAULT_ARGS[
        "mode"
    ],
    data_dir: Annotated[
        pathlib.Path, typer.Option(envvar="LLAMA_INDEX_DATA_DIR")
    ] = DEFAULT_ARGS["data_dir"],
    which_index: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_WHICH_INDEX")
    ] = DEFAULT_ARGS["which_index"],
    force_new_index: Annotated[
        bool, typer.Option(envvar="LLAMA_INDEX_FORCE_NEW_INDEX")
    ] = DEFAULT_ARGS["force_new_index"],
    max_input_size: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_MAX_INPUT_SIZE")
    ] = DEFAULT_ARGS["max_input_size"],
    k: Annotated[int, typer.Option(envvar="LLAMA_INDEX_K")] = DEFAULT_ARGS["k"],
    chunk_size: Annotated[
        Optional[int], typer.Option(envvar="LLAMA_INDEX_CHUNK_SIZE")
    ] = DEFAULT_ARGS.get("chunk_size"),
    chunk_overlap_ratio: Annotated[
        float, typer.Option(envvar="LLAMA_INDEX_CHUNK_OVERLAP_RATIO")
    ] = DEFAULT_ARGS["chunk_overlap_ratio"],
    num_output: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_NUM_OUTPUT")
    ] = DEFAULT_ARGS["num_output"],
    is_path: Annotated[bool, typer.Option(envvar="LLAMA_INDEX_IS_PATH")] = DEFAULT_ARGS[
        "is_path"
    ],
    n_gpu_layers: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_N_GPU_LAYERS")
    ] = DEFAULT_ARGS["n_gpu_layers"],
    device: Annotated[str, typer.Option(envvar="LLAMA_INDEX_DEVICE")] = DEFAULT_ARGS[
        "device"
    ],
) -> None:
    main(
        cli="app",
        model=model,
        model_name=model_name,
        mode=mode,
        data_dir=data_dir,
        which_index=which_index,
        force_new_index=force_new_index,
        max_input_size=max_input_size,
        k=k,
        chunk_size=chunk_size,
        chunk_overlap_ratio=chunk_overlap_ratio,
        num_output=num_output,
        is_path=is_path,
        n_gpu_layers=n_gpu_layers,
        device=device,
    )


@cli.command()
def create_index(
    data_dir: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_DATA_DIR")
    ] = DEFAULT_ARGS["data_dir"],
    which_index: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_WHICH_INDEX")
    ] = DEFAULT_ARGS["which_index"],
    max_input_size: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_MAX_INPUT_SIZE")
    ] = DEFAULT_ARGS["max_input_size"],
    k: Annotated[int, typer.Option(envvar="LLAMA_INDEX_K")] = DEFAULT_ARGS["k"],
    chunk_size: Annotated[
        Optional[int], typer.Option(envvar="LLAMA_INDEX_CHUNK_SIZE")
    ] = DEFAULT_ARGS.get("chunk_size"),
    chunk_overlap_ratio: Annotated[
        float, typer.Option(envvar="LLAMA_INDEX_CHUNK_OVERLAP_RATIO")
    ] = DEFAULT_ARGS["chunk_overlap_ratio"],
    num_output: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_NUM_OUTPUT")
    ] = DEFAULT_ARGS["num_output"],
) -> None:
    main(
        cli="create_index",
        data_dir=data_dir,
        which_index=which_index,
        max_input_size=max_input_size,
        k=k,
        chunk_size=chunk_size,
        chunk_overlap_ratio=chunk_overlap_ratio,
        num_output=num_output,
    )


@cli.command()
def chat(
    model: Annotated[
        str,
        typer.Option(
            envvar="REGINALD_MODEL",
            help="Select which type of model to use. Default is 'hello'.",
        ),
    ] = DEFAULT_ARGS["model"],
    model_name: Annotated[
        Optional[str], typer.Option(envvar="REGINALD_MODEL_NAME")
    ] = None,
    mode: Annotated[str, typer.Option(envvar="LLAMA_INDEX_MODE")] = DEFAULT_ARGS[
        "mode"
    ],
    data_dir: Annotated[
        pathlib.Path, typer.Option(envvar="LLAMA_INDEX_DATA_DIR")
    ] = DEFAULT_ARGS["data_dir"],
    which_index: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_WHICH_INDEX")
    ] = DEFAULT_ARGS["which_index"],
    force_new_index: Annotated[
        bool, typer.Option(envvar="LLAMA_INDEX_FORCE_NEW_INDEX")
    ] = DEFAULT_ARGS["force_new_index"],
    max_input_size: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_MAX_INPUT_SIZE")
    ] = DEFAULT_ARGS["max_input_size"],
    k: Annotated[int, typer.Option(envvar="LLAMA_INDEX_K")] = DEFAULT_ARGS["k"],
    chunk_size: Annotated[
        Optional[int], typer.Option(envvar="LLAMA_INDEX_CHUNK_SIZE")
    ] = DEFAULT_ARGS.get("chunk_size"),
    chunk_overlap_ratio: Annotated[
        float, typer.Option(envvar="LLAMA_INDEX_CHUNK_OVERLAP_RATIO")
    ] = DEFAULT_ARGS["chunk_overlap_ratio"],
    num_output: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_NUM_OUTPUT")
    ] = DEFAULT_ARGS["num_output"],
    is_path: Annotated[bool, typer.Option(envvar="LLAMA_INDEX_IS_PATH")] = DEFAULT_ARGS[
        "is_path"
    ],
    n_gpu_layers: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_N_GPU_LAYERS")
    ] = DEFAULT_ARGS["n_gpu_layers"],
    device: Annotated[str, typer.Option(envvar="LLAMA_INDEX_DEVICE")] = DEFAULT_ARGS[
        "device"
    ],
) -> None:
    main(
        cli="chat",
        model=model,
        model_name=model_name,
        mode=mode,
        data_dir=data_dir,
        which_index=which_index,
        force_new_index=force_new_index,
        max_input_size=max_input_size,
        k=k,
        chunk_size=chunk_size,
        chunk_overlap_ratio=chunk_overlap_ratio,
        num_output=num_output,
        is_path=is_path,
        n_gpu_layers=n_gpu_layers,
        device=device,
    )
