# Standard library imports
import logging
from typing import Optional

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
        if req.type != "events_api":
            logging.info(f"Received unexpected request of type '{req.type}'")
            return None

        # Acknowledge the request
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        try:
            # Extract user and message information
            event = req.payload["event"]
            message = event["text"]
            user_id = event["user"]
            event_type = event["type"]
            event_subtype = event.get("subtype", None)
            sender_is_bot = "bot_id" in event

            # Ignore changes to messages.
            if event_type == "message" and event_subtype == "message_changed":
                logging.info(f"Ignoring changes to messages.")
                return None

            logging.info(f"Received message '{message}' from user '{user_id}'")

            # Ignore messages from bots
            if sender_is_bot:
                logging.info(f"Ignoring messages from bots.")
                return None

            # If this is a direct message to REGinald...
            if event_type == "message" and event_subtype is None:
                self.react(client, event["channel"], event["ts"])
                model_response = self.model.direct_message(message, user_id)

            # If @REGinald is mentioned in a channel
            elif event_type == "app_mention":
                self.react(client, event["channel"], event["ts"])
                model_response = self.model.channel_mention(message, user_id)

            # Otherwise
            else:
                logging.info(f"Received unexpected event of type '{event['type']}'")
                return None

            # Add an emoji and a reply as required
            if model_response and model_response.message:
                logging.info(f"Posting reply {model_response.message}.")
                client.web_client.chat_postMessage(
                    channel=event["channel"], text=model_response.message
                )
            else:
                logging.info(f"No reply was generated.")

        except KeyError as exc:
            logging.warning(f"Attempted to access key that does not exist.\n{str(exc)}")

        except Exception as exc:
            logging.error(
                f"Something went wrong in processing a Slack request.\nPayload: {req.payload}.\n{str(exc)}"
            )
            raise

    def react(self, client: SocketModeClient, channel: str, timestamp: str) -> None:
        """Emoji react to the input message"""
        if self.model.emoji:
            logging.info(f"Reacting with emoji {self.model.emoji}")
            client.web_client.reactions_add(
                name=self.model.emoji,
                channel=channel,
                timestamp=timestamp,
            )
        else:
            logging.info(f"No emoji defined for this model.")
