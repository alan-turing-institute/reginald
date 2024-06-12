import logging

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from reginald.models.setup_llm import setup_llm
from reginald.parser_utils import Parser, get_args


class Query(BaseModel):
    message: str
    user_id: str


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

    # set up FastAPI
    app = FastAPI()

    # set up basic root endpoint
    @app.get("/")
    async def ping():
        return "pong"

    # set up direct_message endpoint
    #
    # See the note on the below 'POST' endpoint and consider deprecating
    @app.get("/direct_message")
    async def direct_message(query: Query):
        return response_model.direct_message(query.message, query.user_id)

    # A POST direct_message endpoint, equivalent to the above.
    # This provides a version of the endpoint that avoids a surprising use of
    # the message body for a GET request.  Provided as an additional endpoint
    # instead of replacing the GET endpoint to avoid breaking things.
    @app.post("/direct_message")
    async def direct_message(query: Query):
        return response_model.direct_message(query.message, query.user_id)

    # set up channel_mention endpoint
    @app.get("/channel_mention")
    async def channel_mention(query: Query):
        response = response_model.channel_mention(query.message, query.user_id)
        return response

    # POST channel_mention endpoint: see comment on direct_message
    @app.post("/channel_mention")
    async def channel_mention(query: Query):
        response = response_model.channel_mention(query.message, query.user_id)
        return response

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
