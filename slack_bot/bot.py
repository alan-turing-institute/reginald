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
    if req.type != "events_api":
        return None

    try:
        event = req.payload["event"]
        text = event["text"]
        user_id = event["user"]
        sender_is_bot = "bot_id" in event
        logging.info(f"Request text: '{text}'")

        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        response = call_and_response(text, user_id)
        # Direct message to REGinald
        if (
            event["type"] == "message"
            and event.get("subtype") is None
            and not sender_is_bot
        ):
            # DM the bot
            client.web_client.reactions_add(
                name="eyes",
                channel=event["channel"],
                timestamp=event["ts"],
            )
            client.web_client.chat_postMessage(channel=event["channel"], text=response)

        # Mention @REGinald in a channel
        elif event["type"] == "app_mention" and not sender_is_bot:
            client.web_client.reactions_add(
                name="+1",
                channel=event["channel"],
                timestamp=event["ts"],
            )
            client.web_client.chat_postMessage(channel=event["channel"], text=response)
    except Exception:
        logging.error(f"Something went wrong in `process`. Payload: {req.payload}")
        raise


if __name__ == "__main__":
    # Initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # This import triggers some non-trivial set up, so we call it here, e.g. after
    # setting up logging.
    from huggingface_backend import call_and_response

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
