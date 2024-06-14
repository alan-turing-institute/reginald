import pathlib
from typing import Final

EMOJI_DEFAULT: Final[str] = "rocket"

LLAMA_INDEX_DIR: Final[str] = "llama_index_indices"

DEFAULT_ARGS = {
    "model": "hello",
    "mode": "chat",
    "data_dir": pathlib.Path(__file__).parent.parent / "data",
    "which_index": "reg",
    "force_new_index": False,
    "max_input_size": 4096,
    "k": 3,
    "chunk_size": 512,
    "chunk_overlap_ratio": 0.1,
    "num_output": 512,
    "is_path": False,
    "n_gpu_layers": 0,
    "device": "auto",
    "host": "0.0.0.0",
    "port": 8000,
}
