import logging

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from reginald.models.setup_llm import setup_llm
from reginald.parser_utils import Parser, get_args


class Query(BaseModel):
    message: str
    user_id: str


def create_reginald_app(response_model) -> FastAPI:
    # set up FastAPI
    app = FastAPI()

    # set up basic root endpoint
    @app.get("/")
    async def ping():
        return "pong"

    # set up direct_message endpoint
    @app.get("/direct_message")
    async def direct_message(query: Query):
        response = response_model.direct_message(query.message, query.user_id)
        return response

    # set up channel_mention endpoint
    @app.get("/channel_mention")
    async def channel_mention(query: Query):
        response = response_model.channel_mention(query.message, query.user_id)
        return response

    return app

def main():
    """
    Main function to run the app which sets up the response model
    and then creates a FastAPI app to serve the model.

    The app listens on port 8000 and has two endpoints:
    - /direct_message: for obtaining responses from direct messages
    - /channel_mention: for obtaining responses from channel mentions
    """
    # parse command line arguments
    parser = Parser()

    # pass args to setup_llm
    args = get_args(parser)

    # initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # set up response model
    response_model = setup_llm(**vars(args))

    app = create_reginald_app(response_model)
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
