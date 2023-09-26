import logging
import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from reginald.models.setup_llm import setup_llm
from reginald.utils import Parser


class Query(BaseModel):
    message: str
    user_id: str


def main():
    # Parse command line arguments
    parser = Parser()

    # pass args to setup_llm
    llm_kwargs = vars(parser.parse_args())

    # Initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # set up response model
    response_model = setup_llm(**llm_kwargs)

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
