import argparse
import pathlib

from reginald.models.models import MODELS
from reginald.utils import get_env_var


class Parser(argparse.ArgumentParser):
    def __init__(self, create_index_only: bool = False, *args, **kwargs):
        """
        Parser for command line arguments for Reginald.

        Note that the default values for the arguments are set to a lambda function
        to obtain the relevant environment variables (if they exist). They are
        lambda functions so that the environment variables are only obtained if
        the argument is actually used.

        See `get_args` for parsing the arguments and obtaining any of the
        environment variables if using default values.

        Parameters
        ----------
        create_index_only : bool, optional
            Whether or not to only include ones related to data index creation,
            by default False
        """
        super().__init__(*args, **kwargs)
        if not create_index_only:
            # model arguments
            self.add_argument(
                "--model",
                "-m",
                type=str,
                help=("Select which type of model to use " "Default is 'hello'."),
                default=lambda: get_env_var("REGINALD_MODEL", secret_value=False),
                choices=MODELS,
            )
            self.add_argument(
                "--model-name",
                "-n",
                type=str,
                help=(
                    "Select which sub-model to use (within the main model selected)."
                    "For llama-index-llama-cpp and llama-index-hf models, this specifies"
                    "the LLM (or path to that model) which we would like to use."
                    "For chat-completion-azure and llama-index-gpt-azure, this refers"
                    "to the deployment name on Azure."
                    "For chat-completion-azure and llama-index-gpt-openai, this refers"
                    "to the model name on OpenAI."
                    "(ignored if using 'hello' model types)."
                ),
                default=lambda: get_env_var("REGINALD_MODEL_NAME", secret_value=False),
            )
            self.add_argument(
                "--mode",
                type=str,
                help=(
                    "Select which mode to use "
                    "(ignored if not using llama-index). "
                    "Default is 'chat'."
                ),
                default=lambda: get_env_var("LLAMA_INDEX_MODE", secret_value=False),
                choices=["chat", "query"],
            )
            self.add_argument(
                "--force-new-index",
                "-f",
                help=(
                    "Recreate the index vector store or not "
                    "(ignored if not using llama-index). "
                    "Default is False."
                ),
                action=argparse.BooleanOptionalAction,
                default=lambda: get_env_var(
                    "LLAMA_INDEX_FORCE_NEW_INDEX", secret_value=False
                ),
            )
            self.add_argument(
                "--is-path",
                "-p",
                help=(
                    "Whether or not the model_name passed is a path to the model "
                    "(ignored if not using llama-index-llama-cpp). "
                    "Default is False."
                ),
                action=argparse.BooleanOptionalAction,
                default=lambda: get_env_var("LLAMA_INDEX_IS_PATH", secret_value=False),
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
                default=lambda: int(
                    get_env_var("LLAMA_INDEX_N_GPU_LAYERS", secret_value=False)
                ),
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
                default=lambda: get_env_var("LLAMA_INDEX_DEVICE", secret_value=False),
            )

        # data index arguments
        self.add_argument(
            "--data-dir",
            "-d",
            type=pathlib.Path,
            help=(
                "Location for data (ignored if not using llama-index). "
                "Default is 'data' in the root of the repo."
            ),
            default=lambda: get_env_var("LLAMA_INDEX_DATA_DIR", secret_value=False)
            or (pathlib.Path(__file__).parent.parent / "data").resolve(),
        )
        self.add_argument(
            "--which-index",
            "-w",
            type=str,
            help=(
                "Specifies the directory name for looking up/writing indices "
                "(ignored if not using llama-index). "
                "Currently supports 'handbook', 'wikis', 'public', or 'all_data'. "
                "Default is 'all_data'."
            ),
            default=lambda: get_env_var("LLAMA_INDEX_WHICH_INDEX", secret_value=False),
            choices=["handbook", "wikis", "public", "all_data"],
        )
        self.add_argument(
            "--max-input-size",
            "-max",
            type=int,
            help=(
                "Select maximum input size for LlamaCPP or HuggingFace model "
                "(ignored if not using llama-index). "
                "Default is 4096."
            ),
            default=lambda: int(
                get_env_var("LLAMA_INDEX_MAX_INPUT_SIZE", secret_value=False)
            ),
        )
        self.add_argument(
            "--k",
            type=int,
            help=(
                "`similarity_top_k` to use in chat or query engine, "
                "(ignored if not using llama-index). "
                "Default is 3."
            ),
            default=lambda: int(get_env_var("LLAMA_INDEX_K", secret_value=False)),
        )
        self.add_argument(
            "--chunk-size",
            "-cs",
            type=int,
            help=(
                "Select chunk size for LlamaIndex model "
                "(ignored if not using llama-index). "
                "Default is computed by ceil(max_input_size / k)."
            ),
            default=lambda: int(
                get_env_var("LLAMA_INDEX_CHUNK_SIZE", secret_value=False)
            ),
        )
        self.add_argument(
            "--chunk-overlap-ratio",
            "-cor",
            type=float,
            help=(
                "Select chunk overlap ratio for LlamaIndex model "
                "(ignored if not using llama-index). "
                "Default is 0.1."
            ),
            default=lambda: float(
                get_env_var("LLAMA_INDEX_CHUNK_OVERLAP_RATIO", secret_value=False)
            ),
        )
        self.add_argument(
            "--num-output",
            "-no",
            type=int,
            help=(
                "Select number of outputs for LlamaIndex LLM model "
                "(ignored if not using llama-index). "
                "Default is 512."
            ),
            default=lambda: int(
                get_env_var("LLAMA_INDEX_NUM_OUTPUT", secret_value=False)
            ),
        )


def get_args(parser: Parser) -> argparse.Namespace:
    """
    Helper function to parse command line arguments and obtain any of the
    environment variables if using default values.

    Parameters
    ----------
    parser : Parser
        Parser for command line arguments for Reginald

    Returns
    -------
    argparse.Namespace
        Namespace of parsed arguments
    """
    # parse command line arguments
    args = parser.parse_args()

    # call any lambda functions in the args
    for arg_name in vars(args):
        arg_value = getattr(args, arg_name)
        if callable(arg_value):
            # call the lambda function to get its value
            arg_value = arg_value()
            # update the argument value in args
            setattr(args, arg_name, arg_value)

    return args
