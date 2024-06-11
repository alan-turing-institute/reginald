from fastapi import FastAPI
from pydantic import BaseModel


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
