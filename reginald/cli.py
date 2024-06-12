import logging
import pathlib
from typing import Annotated, Optional

import typer

from reginald.models.setup_llm import DEFAULT_ARGS
from reginald.run import EMOJI_DEFAULT, main

API_URL_PROPMPT = "No API URL was provided and REGINALD_API_URL not set. Please provide an API URL for the Reginald app"
HELP_TEXT = {
    "model": "Select which type of model to use..",
    "model_name": "Select which sub-model to use (within the main model selected).",
    "data_dir": "Location of the data (ignored if not using llama-index). Default is the data directory in the root of the repo.",
    "which_index": "Which index to use (ignored if not using llama-index).",
    "mode": "Select which mode to use (ignored if not using llama-index).",
    "force_new_index": "Whether to force the creation of a new index (ignored if not using llama-index).",
    "max_input_size": "Maximum input size for the model (ignored if not using llama-index).",
    "k": "'similarity_top_k' to use in chat or query engine (ignored if not using llama-index).",
    "chunk_size": "Chunk size for the model (ignored if not using llama-index).",
    "chunk_overlap_ratio": "Chunk overlap ratio for the model (ignored if not using llama-index).",
    "num_output": "Number of outputs to generate (ignored if not using llama-index).",
    "is_path": "Whether the data is a path (ignored if not using llama-index-llama-cpp).",
    "n_gpu_layers": "Number of GPU layers to use (ignored if not using llama-index).",
    "device": "Device to use (ignored if not using llama-index).",
    "api_url": "API URL for the Reginald app.",
    "emoji": "Emoji to use for the bot.",
}

cli = typer.Typer()


def set_up_logging_config(level: int = 20) -> None:
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=level,
    )


@cli.command()
def run_all(
    model: Annotated[
        str,
        typer.Option(
            envvar="REGINALD_MODEL",
            help=HELP_TEXT["model"],
        ),
    ] = DEFAULT_ARGS["model"],
    model_name: Annotated[
        Optional[str],
        typer.Option(envvar="REGINALD_MODEL_NAME", help=HELP_TEXT["model_name"]),
    ] = None,
    mode: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_MODE", help=HELP_TEXT["mode"])
    ] = DEFAULT_ARGS["mode"],
    data_dir: Annotated[
        pathlib.Path,
        typer.Option(envvar="LLAMA_INDEX_DATA_DIR", help=HELP_TEXT["data_dir"]),
    ] = DEFAULT_ARGS["data_dir"],
    which_index: Annotated[
        str,
        typer.Option(envvar="LLAMA_INDEX_WHICH_INDEX", help=HELP_TEXT["which_index"]),
    ] = DEFAULT_ARGS["which_index"],
    force_new_index: Annotated[
        bool,
        typer.Option(
            envvar="LLAMA_INDEX_FORCE_NEW_INDEX", help=HELP_TEXT["force_new_index"]
        ),
    ] = DEFAULT_ARGS["force_new_index"],
    max_input_size: Annotated[
        int,
        typer.Option(
            envvar="LLAMA_INDEX_MAX_INPUT_SIZE", help=HELP_TEXT["max_input_size"]
        ),
    ] = DEFAULT_ARGS["max_input_size"],
    k: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_K", help=HELP_TEXT["k"])
    ] = DEFAULT_ARGS["k"],
    chunk_size: Annotated[
        Optional[int],
        typer.Option(envvar="LLAMA_INDEX_CHUNK_SIZE", help=HELP_TEXT["chunk_size"]),
    ] = DEFAULT_ARGS.get("chunk_size"),
    chunk_overlap_ratio: Annotated[
        float,
        typer.Option(
            envvar="LLAMA_INDEX_CHUNK_OVERLAP_RATIO",
            help=HELP_TEXT["chunk_overlap_ratio"],
        ),
    ] = DEFAULT_ARGS["chunk_overlap_ratio"],
    num_output: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_NUM_OUTPUT", help=HELP_TEXT["num_output"])
    ] = DEFAULT_ARGS["num_output"],
    is_path: Annotated[
        bool, typer.Option(envvar="LLAMA_INDEX_IS_PATH", help=HELP_TEXT["is_path"])
    ] = DEFAULT_ARGS["is_path"],
    n_gpu_layers: Annotated[
        int,
        typer.Option(envvar="LLAMA_INDEX_N_GPU_LAYERS", help=HELP_TEXT["n_gpu_layers"]),
    ] = DEFAULT_ARGS["n_gpu_layers"],
    device: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_DEVICE", help=HELP_TEXT["device"])
    ] = DEFAULT_ARGS["device"],
) -> None:
    set_up_logging_config(level=20)
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
        str,
        typer.Option(
            prompt=API_URL_PROPMPT, envvar="REGINALD_API_URL", help=HELP_TEXT["api_url"]
        ),
    ],
    emoji: Annotated[
        str, typer.Option(envvar="REGINALD_EMOJI", help=HELP_TEXT["emoji"])
    ] = EMOJI_DEFAULT,
) -> None:
    """
    Main function to run the Slack bot which sets up the bot
    (which uses an API for responding to messages) and
    then establishes a WebSocket connection to the
    Socket Mode servers and listens for events.
    """
    set_up_logging_config(level=20)
    main(
        cli="bot",
        api_url=api_url,
        emoji=emoji,
    )


@cli.command()
def app(
    model: Annotated[
        str,
        typer.Option(
            envvar="REGINALD_MODEL",
            help=HELP_TEXT["model"],
        ),
    ] = DEFAULT_ARGS["model"],
    model_name: Annotated[
        Optional[str],
        typer.Option(envvar="REGINALD_MODEL_NAME", help=HELP_TEXT["model_name"]),
    ] = None,
    mode: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_MODE", help=HELP_TEXT["mode"])
    ] = DEFAULT_ARGS["mode"],
    data_dir: Annotated[
        pathlib.Path,
        typer.Option(envvar="LLAMA_INDEX_DATA_DIR", help=HELP_TEXT["data_dir"]),
    ] = DEFAULT_ARGS["data_dir"],
    which_index: Annotated[
        str,
        typer.Option(envvar="LLAMA_INDEX_WHICH_INDEX", help=HELP_TEXT["which_index"]),
    ] = DEFAULT_ARGS["which_index"],
    force_new_index: Annotated[
        bool,
        typer.Option(
            envvar="LLAMA_INDEX_FORCE_NEW_INDEX", help=HELP_TEXT["force_new_index"]
        ),
    ] = DEFAULT_ARGS["force_new_index"],
    max_input_size: Annotated[
        int,
        typer.Option(
            envvar="LLAMA_INDEX_MAX_INPUT_SIZE", help=HELP_TEXT["max_input_size"]
        ),
    ] = DEFAULT_ARGS["max_input_size"],
    k: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_K", help=HELP_TEXT["k"])
    ] = DEFAULT_ARGS["k"],
    chunk_size: Annotated[
        Optional[int],
        typer.Option(envvar="LLAMA_INDEX_CHUNK_SIZE", help=HELP_TEXT["chunk_size"]),
    ] = DEFAULT_ARGS.get("chunk_size"),
    chunk_overlap_ratio: Annotated[
        float,
        typer.Option(
            envvar="LLAMA_INDEX_CHUNK_OVERLAP_RATIO",
            help=HELP_TEXT["chunk_overlap_ratio"],
        ),
    ] = DEFAULT_ARGS["chunk_overlap_ratio"],
    num_output: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_NUM_OUTPUT", help=HELP_TEXT["num_output"])
    ] = DEFAULT_ARGS["num_output"],
    is_path: Annotated[
        bool, typer.Option(envvar="LLAMA_INDEX_IS_PATH", help=HELP_TEXT["is_path"])
    ] = DEFAULT_ARGS["is_path"],
    n_gpu_layers: Annotated[
        int,
        typer.Option(envvar="LLAMA_INDEX_N_GPU_LAYERS", help=HELP_TEXT["n_gpu_layers"]),
    ] = DEFAULT_ARGS["n_gpu_layers"],
    device: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_DEVICE", help=HELP_TEXT["device"])
    ] = DEFAULT_ARGS["device"],
) -> None:
    """
    Main function to run the app which sets up the response model
    and then creates a FastAPI app to serve the model.

    The app listens on port 8000 and has two endpoints:
    - /direct_message: for obtaining responses from direct messages
    - /channel_mention: for obtaining responses from channel mentions
    """
    set_up_logging_config(level=20)
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
    set_up_logging_config(level=20)
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
            help=HELP_TEXT["model"],
        ),
    ] = DEFAULT_ARGS["model"],
    model_name: Annotated[
        Optional[str],
        typer.Option(envvar="REGINALD_MODEL_NAME", help=HELP_TEXT["model_name"]),
    ] = None,
    mode: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_MODE", help=HELP_TEXT["mode"])
    ] = DEFAULT_ARGS["mode"],
    data_dir: Annotated[
        pathlib.Path,
        typer.Option(envvar="LLAMA_INDEX_DATA_DIR", help=HELP_TEXT["data_dir"]),
    ] = DEFAULT_ARGS["data_dir"],
    which_index: Annotated[
        str,
        typer.Option(envvar="LLAMA_INDEX_WHICH_INDEX", help=HELP_TEXT["which_index"]),
    ] = DEFAULT_ARGS["which_index"],
    force_new_index: Annotated[
        bool,
        typer.Option(
            envvar="LLAMA_INDEX_FORCE_NEW_INDEX", help=HELP_TEXT["force_new_index"]
        ),
    ] = DEFAULT_ARGS["force_new_index"],
    max_input_size: Annotated[
        int,
        typer.Option(
            envvar="LLAMA_INDEX_MAX_INPUT_SIZE", help=HELP_TEXT["max_input_size"]
        ),
    ] = DEFAULT_ARGS["max_input_size"],
    k: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_K", help=HELP_TEXT["k"])
    ] = DEFAULT_ARGS["k"],
    chunk_size: Annotated[
        Optional[int],
        typer.Option(envvar="LLAMA_INDEX_CHUNK_SIZE", help=HELP_TEXT["chunk_size"]),
    ] = DEFAULT_ARGS.get("chunk_size"),
    chunk_overlap_ratio: Annotated[
        float,
        typer.Option(
            envvar="LLAMA_INDEX_CHUNK_OVERLAP_RATIO",
            help=HELP_TEXT["chunk_overlap_ratio"],
        ),
    ] = DEFAULT_ARGS["chunk_overlap_ratio"],
    num_output: Annotated[
        int, typer.Option(envvar="LLAMA_INDEX_NUM_OUTPUT", help=HELP_TEXT["num_output"])
    ] = DEFAULT_ARGS["num_output"],
    is_path: Annotated[
        bool, typer.Option(envvar="LLAMA_INDEX_IS_PATH", help=HELP_TEXT["is_path"])
    ] = DEFAULT_ARGS["is_path"],
    n_gpu_layers: Annotated[
        int,
        typer.Option(envvar="LLAMA_INDEX_N_GPU_LAYERS", help=HELP_TEXT["n_gpu_layers"]),
    ] = DEFAULT_ARGS["n_gpu_layers"],
    device: Annotated[
        str, typer.Option(envvar="LLAMA_INDEX_DEVICE", help=HELP_TEXT["device"])
    ] = DEFAULT_ARGS["device"],
) -> None:
    set_up_logging_config(level=40)
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
