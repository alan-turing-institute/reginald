from fastapi import FastAPI
from pydantic import BaseModel
from setup_llm import setup_llm


class Query(BaseModel):
    message: str
    user_id: str


response_model = setup_llm()
app = FastAPI()


@app.get("/")
async def root():
    return "Hello World"


@app.get("/direct_message")
async def direct_message(query: Query):
    response = response_model.direct_message(query.message, query.user_id)
    return response


@app.get("/channel_mention")
async def channel_mention(query: BaseModel):
    response = response_model.channel_mention(query.message, query.user_id)
    return response
