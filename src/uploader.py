# src/uploader.py
import json
import os
from tqdm import tqdm

from src.api.dataset_api import upload_file, import_dataset


def update_json_data_with_urls(json_data, file_urls):
    """
    Update the JSON data with the corresponding file URLs.

    Args:
        json_data (list): The JSON data to be updated.
        file_urls (dict): A dictionary mapping file names to their URLs.
    """
    for item in json_data:
        file_key = (
            item["data"].get("image")
            or item["data"].get("video")
            or item["data"].get("file")
            or item["data"].get("audio")
        )
        if file_key:
            file_name = os.path.basename(file_key)
            if file_name in file_urls:
                item["data"]["file"] = file_urls[file_name]


def upload_dataset(temp_output_folder, dataset_id, api_key):
    """
    Uploads a dataset to a specified location using the provided API key.

    Args:
        temp_output_folder (str): The temporary output folder containing the dataset files.
        dataset_id (str): The ID of the dataset to upload.
        api_key (str): The API key used for authentication.

    Raises:
        FileNotFoundError: If a file to be uploaded does not exist.
        Exception: If the JSON data fails to be posted.

    Returns:
        None
    """
    json_file_path = os.path.join(temp_output_folder, "dataset.json")
    with open(json_file_path, "r") as file:
        json_data = json.load(file)

    file_urls = {}

    # Prepare a list of files to upload
    files_to_upload = []
    for item in json_data:
        file_key = (
            item["data"].get("image")
            or item["data"].get("video")
            or item["data"].get("file")
            or item["data"].get("audio")
        )
        if file_key:
            file_name = os.path.basename(file_key)
            files_to_upload.append(file_name)

    # Iterate over files with a progress bar
    for file_name in tqdm(files_to_upload, desc="Uploading files"):
        file_path = os.path.join(temp_output_folder, "files", file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")
        url = upload_file(file_path, api_key, dataset_id)
        file_urls[file_name] = url

    update_json_data_with_urls(json_data, file_urls)

    json_data_path = os.path.join(temp_output_folder, "dataset_processed.json")
    with open(json_data_path, "w") as f:
        json.dump(json_data, f, indent=4)

    response = import_dataset(json_data_path, api_key, dataset_id)

    if response.status_code != 200:
        raise Exception(f"Failed to post JSON data: {response.text}")
    print(f"Dataset imported successfully: {response.status_code}, {response.text}")
