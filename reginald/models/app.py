import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from reginald.models.setup_llm import setup_llm


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

    # POST channel_mention endpoint: see comment on direct_message
    @app.post("/channel_mention")
    async def channel_mention(query: Query):
        response = response_model.channel_mention(query.message, query.user_id)
        return response

    return app


async def run_reginald_app(**kwargs) -> None:
    # set up response model
    response_model = setup_llm(**kwargs)
    app: FastAPI = create_reginald_app(response_model)
    uvicorn.run(app, host="0.0.0.0", port=8000)
