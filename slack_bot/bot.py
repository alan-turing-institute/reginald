# Standard library imports
import logging
import os
import threading

# Third-party imports
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.web import WebClient


def process(client: SocketModeClient, req: SocketModeRequest) -> None:
    logging.info(f"Received request of type '{req.type}'")
    if req.type == "events_api":
        logging.info(f"Request text: '{req.payload['event']['text']}'")

        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        # Direct message to REGinald
        if (
            req.payload["event"]["type"] == "message"
            and req.payload["event"].get("subtype") is None
        ):
            # DM the bot
            client.web_client.reactions_add(
                name="eyes",
                channel=req.payload["event"]["channel"],
                timestamp=req.payload["event"]["ts"],
            )

        # Mention @REGinald in a channel
        elif req.payload["event"]["type"] == "app_mention":
            client.web_client.reactions_add(
                name="+1",
                channel=req.payload["event"]["channel"],
                timestamp=req.payload["event"]["ts"],
            )
            user_id = req.payload["event"]["user"]
            client.web_client.chat_postMessage(
                channel=req.payload["event"]["channel"], text=f"Hello <@{user_id}>!"
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
        app_token=os.environ.get("SLACK_APP_TOKEN"),  # xapp-A111-222-xyz
        # You will be using this WebClient for performing Web API calls in listeners
        web_client=WebClient(
            token=os.environ.get("SLACK_BOT_TOKEN")
        ),  # xoxb-111-222-xyz
    )

    # Add a new listener to receive messages from Slack
    # You can add more listeners like this
    client.socket_mode_request_listeners.append(process)
    # Establish a WebSocket connection to the Socket Mode servers
    client.connect()

    # Listen for events
    logging.info("Listening for requests...")
    threading.Event().wait()
