# Standard library imports
import logging

# Third-party imports
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.listeners import SocketModeRequestListener
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

# Local imports
from slack_bot.models import ResponseModel


class Bot(SocketModeRequestListener):
    def __init__(self, model: ResponseModel) -> None:
        self.model = model

    def __call__(self, client: SocketModeClient, req: SocketModeRequest) -> None:
        logging.info(f"Received request of type '{req.type}'")
        if req.type == "events_api":
            message = req.payload["event"]["text"]
            user_id = req.payload["event"]["user"]
            logging.info(f"Received message '{message}' from user '{user_id}'")

            # Acknowledge the request anyway
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

            # Direct message to REGinald
            if (
                req.payload["event"]["type"] == "message"
                and req.payload["event"].get("subtype") is None
            ):
                response = self.model.direct_message(message, user_id)

            # Mention @REGinald in a channel
            elif req.payload["event"]["type"] == "app_mention":
                response = self.model.channel_mention(message, user_id)

            # Add an emoji and a reply as required
            if response.emoji:
                logging.info(f"Applying emoji {response.emoji}")
                client.web_client.reactions_add(
                    name=response.emoji,
                    channel=req.payload["event"]["channel"],
                    timestamp=req.payload["event"]["ts"],
                )
            if response.message:
                logging.info(f"Posting message {response.message}")
                client.web_client.chat_postMessage(
                    channel=req.payload["event"]["channel"], text=response.message
                )
