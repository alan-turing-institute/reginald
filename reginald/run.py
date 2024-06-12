import asyncio
import logging
import pathlib
import sys
from typing import Final

import uvicorn
from fastapi import FastAPI
from slack_sdk.socket_mode.aiohttp import SocketModeClient

from reginald.models.app import create_reginald_app
from reginald.models.create_index import create_index
from reginald.models.models.base import ResponseModel
from reginald.models.setup_llm import setup_llm
from reginald.slack_bot.setup_bot import (
    EMOJI_DEFAULT,
    setup_api_slack_bot,
    setup_slack_bot,
    setup_slack_client,
)
from reginald.utils import create_folder

LISTENING_MSG: Final[str] = "Listening for requests..."


async def run_bot(api_url: str | None, emoji: str) -> None:
    if api_url is None:
        logging.error("api_url is not set.")
        sys.exit(1)

    # set up slack bot
    bot = setup_api_slack_bot(api_url=api_url, emoji=emoji)

    # set up slack client
    client = setup_slack_client(slack_bot=bot)
    await connect_client(client)


async def run_reginald_app(**kwargs) -> None:
    # set up response model
    response_model = setup_llm(**kwargs)
    app: FastAPI = create_reginald_app(response_model)
    uvicorn.run(app, host="0.0.0.0", port=8000)


async def run_full_pipeline(**kwargs) -> None:
    # set up response model
    response_model = setup_llm(**kwargs)
    bot = setup_slack_bot(response_model)
    # set up slack client
    client = setup_slack_client(bot)
    await connect_client(client)


def run_chat_interact(streaming: bool = False, **kwargs) -> ResponseModel:
    # set up response model
    response_model = setup_llm(**kwargs)
    user_id = "command_line_chat"

    while True:
        message = input(">>> ")
        if message in ["exit", "exit()", "quit()", "bye Reginald"]:
            return response_model
        if message in ["clear_history", "\clear_history"]:
            if (
                response_model.mode == "chat"
                and response_model.chat_engine.get(user_id) is not None
            ):
                response_model.chat_engine[user_id].reset()
                print("\nReginald: History cleared.")
            else:
                print("\nReginald: No history to clear.")
            continue

        if streaming:
            response = response_model.stream_message(message=message, user_id=user_id)
            print("")
        else:
            response = response_model.direct_message(message=message, user_id=user_id)
            print(f"\nReginald: {response.message}")


async def connect_client(client: SocketModeClient) -> None:
    await client.connect()
    # listen for events
    logging.info(LISTENING_MSG)
    # TODO: Assess whether this is best to use
    await asyncio.sleep(float("inf"))


def download_from_fileshare(
    data_dir: pathlib.Path | str,
    which_index: str,
    azure_storage_key: str | None,
    connection_str: str | None,
) -> None:
    from azure.storage.fileshare import ShareClient
    from tqdm import tqdm

    if azure_storage_key is None:
        logging.error("azure_storage_key is not set.")
        sys.exit(1)
    if connection_str is None:
        logging.error("connection_str is not set.")
        sys.exit(1)

    # set the file share name and directory
    file_share_name = "llama-data"
    file_share_directory = f"llama_index_indices/{which_index}"

    # create a ShareClient object
    share_client = ShareClient.from_connection_string(
        conn_str=connection_str,
        share_name=file_share_name,
        credential=azure_storage_key,
    )

    # get a reference to the file share directory
    file_share_directory_client = share_client.get_directory_client(
        file_share_directory
    )

    # set the local download directory
    local_download_directory = (
        pathlib.Path(data_dir) / "llama_index_indices" / which_index
    )

    # create folder if does not exist
    create_folder(local_download_directory)

    # list all the files in the directory
    files_list = file_share_directory_client.list_directories_and_files()

    # check if the index exists
    try:
        files_list = list(files_list)
    except:
        logging.error(f"Index {which_index} does not exist in the file share")
        sys.exit(1)

    # iterate through each file in the list and download it
    for file in tqdm(files_list):
        if not file.is_directory:
            file_client = file_share_directory_client.get_file_client(file.name)
            download_path = local_download_directory / file.name
            with open(download_path, "wb") as file_handle:
                data = file_client.download_file()
                data.readinto(file_handle)


def main(
    cli: str,
    api_url: str | None = None,
    emoji: str = EMOJI_DEFAULT,
    streaming: bool = False,
    data_dir: str | None = None,
    which_index: str | None = None,
    **kwargs,
):
    # initialise logging
    if cli == "run_all":
        asyncio.run(run_full_pipeline(**kwargs))
    elif cli == "bot":
        asyncio.run(run_bot(api_url=api_url, emoji=emoji))
    elif cli == "app":
        asyncio.run(run_reginald_app(**kwargs))
    elif cli == "chat":
        run_chat_interact(streaming=streaming, **kwargs)
    elif cli == "create_index":
        create_index(**kwargs)
    elif cli == "download":
        download_from_fileshare(data_dir=data_dir, which_index=which_index, **kwargs)
    else:
        logging.info("No run options selected.")


if __name__ == "__main__":
    main()
