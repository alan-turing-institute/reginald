import argparse
import os
import pathlib

from reginald.models.models import MODELS


class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # model args
        self.add_argument(
            "--model",
            "-m",
            help=("Select which type of model to use " "Default is 'hello'."),
            default=os.environ.get("REGINALD_MODEL"),
            choices=MODELS,
        )
        self.add_argument(
            "--model-name",
            "-n",
            type=str,
            help=(
                "Select which model to use "
                "(ignored if using 'hello' or OpenAI model types)."
            ),
            default=os.environ.get("REGINALD_MODEL_NAME"),
        )
        self.add_argument(
            "--mode",
            type=str,
            help=(
                "Select which mode to use "
                "(ignored if not using llama-index). "
                "Default is 'chat'."
            ),
            default=os.environ.get("LLAMA_INDEX_MODE"),
            choices=["chat", "query"],
        )
        self.add_argument(
            "--data-dir",
            "-d",
            type=pathlib.Path,
            help="Location for data",
            default=os.environ.get("LLAMA_INDEX_DATA_DIR")
            or (pathlib.Path(__file__).parent.parent / "data").resolve(),
        )
        self.add_argument(
            "--which-index",
            "-w",
            type=str,
            help=(
                "Specifies the directory name for looking up/writing indices. "
                "Currently supports 'handbook', 'wikis', 'public', or 'all_data'. "
                "Default is 'all_data'."
            ),
            default=os.environ.get("LLAMA_INDEX_WHICH_INDEX"),
            choices=["handbook", "wikis", "public", "all_data"],
        )
        self.add_argument(
            "--force-new-index",
            "-f",
            help="Recreate the index vector store or not",
            action=argparse.BooleanOptionalAction,
            default=os.environ.get("LLAMA_INDEX_FORCE_NEW_INDEX"),
        )
        self.add_argument(
            "--max-input-size",
            "-max",
            type=int,
            help=(
                "Select maximum input size for LlamaCPP or HuggingFace model "
                "(ignored if not using llama-index-llama-cpp or llama-index-hf). "
                "Default is 4096."
            ),
            default=os.environ.get("LLAMA_INDEX_MAX_INPUT_SIZE"),
        )
        self.add_argument(
            "--is-path",
            "-p",
            help=(
                "Whether or not the model_name passed is a path to the model "
                "(ignored if not using llama-index-llama-cpp)"
            ),
            action=argparse.BooleanOptionalAction,
            default=os.environ.get("LLAMA_INDEX_IS_PATH"),
        )
        self.add_argument(
            "--n-gpu-layers",
            "-ngl",
            type=int,
            help=(
                "Select number of GPU layers for LlamaCPP model "
                "(ignored if not using llama-index-llama-cpp). "
                "Default is 0."
            ),
            default=os.environ.get("LLAMA_INDEX_N_GPU_LAYERS"),
        )
        self.add_argument(
            "--device",
            "-dev",
            type=str,
            help=(
                "Select device for HuggingFace model "
                "(ignored if not using llama-index-hf model). "
                "Default is 'auto'."
            ),
            default=os.environ.get("LLAMA_INDEX_DEVICE"),
        )
