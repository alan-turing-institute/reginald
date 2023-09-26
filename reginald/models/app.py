import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from reginald.models.setup_llm import setup_llm


class Query(BaseModel):
    message: str
    user_id: str


def api_setup_llm():
    # set up response model using environment variables
    # defaults for variables get set in setup_llm if any of these are None
    response_model = setup_llm(
        model=os.environ.get("REGINALD_MODEL"),
        model_name=os.environ.get("REGINALD_MODEL_NAME"),
        mode=os.environ.get("LLAMA_INDEX_MODE"),
        data_dir=os.environ.get("LLAMA_INDEX_DATA_DIR"),
        which_index=os.environ.get("LLAMA_INDEX_WHICH_INDEX"),
        force_new_index=os.environ.get("LLAMA_INDEX_FORCE_NEW_INDEX"),
        max_input_size=os.environ.get("LLAMA_INDEX_MAX_INPUT_SIZE"),
        is_path=os.environ.get("LLAMA_INDEX_IS_PATH"),
        n_gpu_layers=os.environ.get("LLAMA_INDEX_N_GPU_LAYERS"),
        device=os.environ.get("LLAMA_INDEX_DEVICE"),
    )

    return response_model


def main():
    # set up response model using environment variables
    response_model = api_setup_llm()
    # set up FastAPI
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

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
