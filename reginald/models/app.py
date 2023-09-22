import os
import pathlib

from fastapi import FastAPI
from pydantic import BaseModel

from reginald.models.models import DEFAULTS
from reginald.models.setup_llm import setup_llm


class Query(BaseModel):
    message: str
    user_id: str


def api_setup_llm():
    kwargs = {}

    # choose model
    kwargs["model"] = os.environ.get("REGINALD_MODEL") or "hello"
    kwargs["model"] = kwargs["model"].lower()

    # set up variables
    kwargs["mode"] = os.environ.get("LLAMA_INDEX_MODE") or "chat"
    kwargs["max_input_size"] = os.environ.get("LLAMA_INDEX_MAX_INPUT_SIZE") or 4096
    kwargs["n_gpu_layers"] = os.environ.get("LLAMA_INDEX_N_GPU_LAYERS") or 0
    kwargs["device"] = os.environ.get("LLAMA_INDEX_DEVICE") or "auto"
    kwargs["data_dir"] = (
        pathlib.Path(os.environ.get("LLAMA_INDEX_DATA_DIR")).resolve()
        or (pathlib.Path(__file__).parent.parent / "data").resolve()
    )
    kwargs["which_index"] = os.environ.get("LLAMA_INDEX_WHICH_INDEX") or "all_data"
    force_new_index = os.environ.get("LLAMA_INDEX_FORCE_NEW_INDEX")
    kwargs["force_new_index"] = (
        (force_new_index.lower() == "true") if force_new_index else False
    )
    if kwargs["model"] in [
        "chat-completion-azure",
        "llama-index-llama-cpp",
        "llama-index-hf",
        "llama-index-gpt-azure",
    ]:
        kwargs["model_name"] = (
            os.environ.get("LLAMA_INDEX_MODEL_NAME") or DEFAULTS[kwargs["model"]]
        )

    response_model = setup_llm(**kwargs)
    return response_model


response_model = api_setup_llm()
app = FastAPI()


@app.get("/")
async def root():
    return "Hello World"


@app.get("/direct_message")
async def direct_message(query: Query):
    response = response_model.direct_message(query.message, query.user_id)
    return response


@app.get("/channel_mention")
async def channel_mention(query: Query):
    response = response_model.channel_mention(query.message, query.user_id)
    return response
