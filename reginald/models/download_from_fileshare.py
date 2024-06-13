import logging
import pathlib
import sys

from reginald.utils import create_folder


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
