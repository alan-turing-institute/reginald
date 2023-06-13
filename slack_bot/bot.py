# Standard library imports
import logging
import os
import threading

# Third-party imports
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.web import WebClient

# Local imports
from strategies import Hello


def process(client: SocketModeClient, req: SocketModeRequest) -> None:
    logging.info(f"Received request of type '{req.type}'")
    if req.type == "events_api":
        message = req.payload["event"]["text"]
        user_id = req.payload["event"]["user"]
        logging.info(f"Received message '{message}' from user '{user_id}'")

        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        responder = Hello()

        # Direct message to REGinald
        if (
            req.payload["event"]["type"] == "message"
            and req.payload["event"].get("subtype") is None
        ):
            response = responder.direct_message(message, user_id)

        # Mention @REGinald in a channel
        elif req.payload["event"]["type"] == "app_mention":
            response = responder.channel_mention(message, user_id)

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


if __name__ == "__main__":
    # Initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # Initialize SocketModeClient with an app-level token + WebClient
    client = SocketModeClient(
        # This app-level token will be used only for establishing a connection
        app_token=os.environ.get("SLACK_APP_TOKEN"),
        # You will be using this WebClient for performing Web API calls in listeners
        web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN")),
    )

    # Add a new listener to receive messages from Slack
    # You can add more listeners like this
    client.socket_mode_request_listeners.append(process)
    # Establish a WebSocket connection to the Socket Mode servers
    client.connect()

    # Listen for events
    logging.info("Listening for requests...")
    threading.Event().wait()
