import requests
from tqdm import tqdm

from ..config.logging import logger
from ..config.urls import DATASET_IMPORT_URL, DATASET_UPLOAD_URL, DATASET_UPDATE_URL, DATASET_CREATE_URL
from ..utilities.api import retry

MAX_FILES = 10  # Maximum number of files per batch

@retry
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

@retry
def upload_files_in_batches(file_paths, api_key, dataset_id):
    """
    Uploads multiple files to the dataset in batches, with a progress bar showing total files.

    Args:
        file_paths (list of str): The paths of the files to be uploaded.
        api_key (str): The API key for authentication.
        dataset_id (str): The ID of the dataset.

    Returns:
        list of str: The URLs of the uploaded files.

    Raises:
        Exception: If the file upload fails.
    """
    uploaded_urls = []

    with tqdm(total=len(file_paths), desc="Uploading files") as pbar:
        for i in range(0, len(file_paths), MAX_FILES):
            batch = file_paths[i:i + MAX_FILES]
            logger.info(f"Uploading file batch: {batch}...")
            url = DATASET_UPLOAD_URL.format(dataset_id=dataset_id)
            headers = {"Authorization": f"Bearer {api_key}"}

            with requests.Session() as session:
                files = [("files", (open(file_path, "rb"))) for file_path in batch]
                response = session.post(url, headers=headers, files=files)

                # Closing opened files
                for _, file in files:
                    file.close()

                if response.status_code != 200:
                    raise Exception(f"Failed to upload files: {response.text}")

                uploaded_urls.extend(response.json()["urls"])

            pbar.update(len(batch))  # Update the progress bar based on the number of files in the batch

    return uploaded_urls

@retry
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

@retry
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

@retry
def create_dataset(name, description, project_id, input_type, action_type, api_key, metadata=None):
    """
    Creates a dataset by sending a POST request to the specified API endpoint.

    Args:
        name (str): The name of the dataset to be created.
        description (str): The description of the dataset to be created.
        project_id (str): The ID of the project to which the dataset belongs.
        input_type (str): The input type of the dataset to be created.
        action_type (str): The action type of the dataset to be created.
        api_key (str): The API key for authentication.

    Returns:
        requests.Response: The response object containing the result of the create request.

    Raises:
        Exception: If the create request fails with a non-200 status code.
    """
    url = DATASET_CREATE_URL
    dataset = {
        "name": name,
        "description": description,
        "project_id": project_id,
        "input_type": input_type,
        "action_type": action_type,
        "metadata": metadata
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, headers=headers, json=dataset)
    if response.status_code != 200:
        raise Exception(f"Failed to create dataset: {response.text}")
    else:
        logger.info(f"Created new dataset with ID: {response.json()['dataset']['id']}")
    return response
