import requests
from src.config.logging import logger
from src.config.urls import DATASET_IMPORT_URL, DATASET_UPLOAD_URL, DATASET_UPDATE_URL


def upload_file(file_path, api_key, dataset_id):
    """
    Uploads a file to the dataset.

    Args:
        file_path (str): The path of the file to be uploaded.
        api_key (str): The API key for authentication.
        dataset_id (str): The ID of the dataset.

    Returns:
        str: The URL of the uploaded file.

    Raises:
        Exception: If the file upload fails.
    """
    logger.info(f"Uploading file {file_path}...")
    # Format the URL with the actual dataset ID
    url = DATASET_UPLOAD_URL.format(dataset_id=dataset_id)
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(file_path, "rb") as file:
        response = requests.post(url, headers=headers, files={"files": file})
    if response.status_code != 200:
        raise Exception(f"Failed to upload file {file_path}: {response.text}")
    return response.json()["urls"][0]


def import_dataset(json_data_path, api_key, dataset_id):
    """
    Imports a dataset by sending a POST request to the specified API endpoint.

    Args:
        json_data_path (str): The path to the JSON data file to be imported.
        api_key (str): The API key for authentication.
        dataset_id (str): The ID of the dataset to import.

    Returns:
        requests.Response: The response object containing the result of the import request.

    Raises:
        Exception: If the import request fails with a non-200 status code.
    """
    url = url = DATASET_IMPORT_URL.format(dataset_id=dataset_id)
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(json_data_path, "rb") as file:
        response = requests.post(url, headers=headers, files={"file": file})
    if response.status_code != 200:
        raise Exception(f"Failed to upload file {json_data_path}: {response.text}")
    return response


def update_dataset(dataset, api_key, dataset_id):
    """
    Updates a dataset by sending a PATCH request to the specified API endpoint.

    Args:
        dataset_metadata (dict): The metadata of the dataset to be updated.
        api_key (str): The API key for authentication.
        dataset_id (str): The ID of the dataset to update.

    Returns:
        requests.Response: The response object containing the result of the update request.

    Raises:
        Exception: If the update request fails with a non-200 status code.
    """
    url = DATASET_UPDATE_URL.format(dataset_id=dataset_id)
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.patch(url, headers=headers, json=dataset)
    if response.status_code != 200:
        raise Exception(f"Failed to update dataset {dataset_id}: {response.text}")
    return response
