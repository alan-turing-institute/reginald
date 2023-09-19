import asyncio
import logging

from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.async_listeners import AsyncSocketModeRequestListener
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

from ..models.base import ResponseModel


class Bot(AsyncSocketModeRequestListener):
    def __init__(self, model: ResponseModel) -> None:
        self.model = model
        self.queue = asyncio.Queue(maxsize=10)

    async def __call__(self, client: SocketModeClient, req: SocketModeRequest) -> None:
        self.queue.put_nowait(self._process_request(client, req))
        logging.info(f"There are currently {self.queue.qsize()} items in the queue.")

        # Create three worker tasks to process the queue concurrently.
        tasks = []
        for i in range(3):
            task = asyncio.create_task(self.worker(self.queue))
            tasks.append(task)

        # await self.queue.join()

        # for task in tasks:
        #     task.cancel()

    @staticmethod
    async def worker(queue):
        while True:
            coro = await queue.get()
            await coro
            # Notify the queue that the "work item" has been processed.
            queue.task_done()

    async def _process_request(
        self, client: SocketModeClient, req: SocketModeRequest
    ) -> None:
        if req.type != "events_api":
            logging.info(f"Received unexpected request of type '{req.type}'")
            return None

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
                return None
            if event.get("hidden") is not None:
                logging.info("Ignoring hidden message.")
                return None

            # Extract user and message information
            message = event["text"]
            user_id = event["user"]
            event_type = event["type"]
            event_subtype = event.get("subtype", None)

            # Start processing the message
            logging.info(f"Processing message '{message}' from user '{user_id}'.")

            # If this is a direct message to REGinald...
            if event_type == "message" and event_subtype is None:
                await self.react(client, event["channel"], event["ts"])
                model_response = self.model.respond(message, user_id)

            # If @REGinald is mentioned in a channel
            elif event_type == "app_mention":
                await self.react(client, event["channel"], event["ts"])
                model_response = self.model.respond(message, user_id)

            # Otherwise
            else:
                logging.info(f"Received unexpected event of type '{event['type']}'.")
                return None

            # Add a reply as required
            if model_response and model_response.message:
                logging.info(f"Posting reply {model_response.message}.")
                await client.web_client.chat_postMessage(
                    channel=event["channel"],
                    text=f"<@{user_id}>, you asked me: '{message}'.\n{model_response.message}",
                )
            else:
                logging.info("No reply was generated.")

        except KeyError as exc:
            logging.warning(f"Attempted to access key that does not exist.\n{str(exc)}")

        except Exception as exc:
            logging.error(
                f"Something went wrong in processing a Slack request.\nPayload: {req.payload}.\n{str(exc)}"
            )
            raise

    async def react(
        self, client: SocketModeClient, channel: str, timestamp: str
    ) -> None:
        """Emoji react to the input message"""
        if self.model.emoji:
            logging.info(f"Reacting with emoji {self.model.emoji}.")
            await client.web_client.reactions_add(
                name=self.model.emoji,
                channel=channel,
                timestamp=timestamp,
            )
        else:
            logging.info("No emoji defined for this model.")
