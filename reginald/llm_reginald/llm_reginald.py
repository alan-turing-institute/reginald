import uuid
import httpx
import llm
from urllib.parse import urljoin
from typing import Optional
from pydantic import Field


@llm.hookimpl
def register_models(register):
    register(Reginald())


class Reginald(llm.Model):
    model_id = "reginald"
    can_stream = False

    class Options(llm.Options):
        server_url: str = Field(
            default="http://localhost:8000",
            title="Server URL",
            description="The base URL of the Reginald server"
        )

        def direct_message_endpoint(self):
            return urljoin(self.server_url, "direct_message")


    def execute(self, prompt, stream, response, conversation):

        message = prompt.prompt

        # Reginald keeps a separate conversation history for each
        # "user_id".  If 'conversation' is None (or doesn't have the
        # user_id logged) start a new conversation by minting a new
        # user_id history.  Otherwise, extract the logged user_id to
        # continue that conversation.

        try:
            user_id = conversation.responses[0].response_json['user_id']
        except (TypeError, AttributeError, KeyError, IndexError) as e:
            user_id = str(uuid.uuid4().int)

        try:
            with httpx.Client() as client:
                reginald_reply = client.post(
                    prompt.options.direct_message_endpoint(),
                    json={"message": message, "user_id": user_id},
                    timeout=None
                )
            reginald_reply.raise_for_status()
        except httpx.HTTPError as e:
            # re-raise as an llm.ModelError for llm to report
            raise llm.ModelError(f"Could not connect to Reginald at {prompt.options.direct_message_endpoint()}.\n\nThe error was:\n    {e}.\n\nIs the model server running?")

        yield reginald_reply.json()['message']

        response.response_json = {'user_id': user_id}
