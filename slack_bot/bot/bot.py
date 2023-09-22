import asyncio
import logging
import os
from ast import mod

import requests
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.async_listeners import AsyncSocketModeRequestListener
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse


class Bot(AsyncSocketModeRequestListener):
    def __init__(self, api_url: str, emoji: str) -> None:
        """TODO: Fill in here

        Parameters
        ----------
        api_url : str
            The api url of the model
        emoji : str
            The emoji to use when responding to a direct message/channel mention.
        """
        self.api_url = api_url
        self.emoji = emoji

        # set up queue and task
        self.queue = asyncio.Queue(maxsize=12)
        _ = asyncio.create_task(self.worker(self.queue))

    async def __call__(self, client: SocketModeClient, req: SocketModeRequest) -> None:
        if req.type != "events_api":
            logging.info(f"Received unexpected request of type '{req.type}'")
            return

        # Acknowledge the request
        logging.info("Received an events_api request")
        response = SocketModeResponse(envelope_id=req.envelope_id)
        await client.send_socket_mode_response(response)

        try:
            # Extract event from payload
            event = req.payload["event"]

            # Ignore messages from bots
            if event.get("bot_id") is not None:
                logging.info("Ignoring an event triggered by a bot.")
                return
            if event.get("hidden") is not None:
                logging.info("Ignoring hidden message.")
                return

            # add clock emoji
            logging.info("Reacting with clock emoji.")
            await client.web_client.reactions_add(
                name="clock2",
                channel=event["channel"],
                timestamp=event["ts"],
            )

            self.queue.put_nowait((client, event))
            logging.info(
                f"There are currently {self.queue.qsize()} items in the queue."
            )

        except KeyError as exc:
            logging.warning(f"Attempted to access key that does not exist.\n{str(exc)}")

        except Exception as exc:
            logging.error(
                f"Something went wrong in processing a Slack request.\nPayload: {req.payload}.\n{str(exc)}"
            )
            raise

    async def worker(self, queue):
        while True:
            (client, event) = await queue.get()
            await self._process_request(client, event)
            # Notify the queue that the "work item" has been processed.
            queue.task_done()

    async def _process_request(
        self,
        client: SocketModeClient,
        event: str,
    ) -> None:
        # Extract user and message information
        message = event["text"]
        user_id = event["user"]
        event_type = event["type"]
        event_subtype = event.get("subtype", None)

        # Start processing the message
        logging.info(f"Processing message '{message}' from user '{user_id}'.")

        await client.web_client.reactions_remove(
            name="clock2",
            channel=event["channel"],
            timestamp=event["ts"],
        )

        # If this is a direct message to REGinald...
        if event_type == "message" and event_subtype is None:
            await self.react(client, event["channel"], event["ts"])
            model_response = requests.get(
                f"{self.api_url}/direct_message",
                json={"message": message, "user_id": user_id},
            )

        # If @REGinald is mentioned in a channel
        elif event_type == "app_mention":
            await self.react(client, event["channel"], event["ts"])
            model_response = requests.get(
                f"{self.api_url}/channel_mention",
                json={"message": message, "user_id": user_id},
            )

        # Otherwise
        else:
            logging.info(f"Received unexpected event of type '{event['type']}'.")
            return

        if model_response.status_code != 200:
            raise ValueError("Unable to get response.")
        model_response = model_response.json()

        # Add a reply as required
        if model_response and model_response["message"]:
            logging.info(f"Posting reply {model_response['message']}.")
            await client.web_client.chat_postMessage(
                channel=event["channel"],
                text=f"<@{user_id}>, you asked me: '{message}'.\n{model_response['message']}",
            )
        else:
            logging.info("No reply was generated.")

    async def react(
        self, client: SocketModeClient, channel: str, timestamp: str
    ) -> None:
        """Emoji react to the input message"""
        if self.emoji:
            logging.info(f"Reacting with emoji {self.emoji}.")
            await client.web_client.reactions_add(
                name=self.emoji,
                channel=channel,
                timestamp=timestamp,
            )
        else:
            logging.info("No emoji defined for this bot.")
