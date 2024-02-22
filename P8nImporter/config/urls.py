# config/api_urls.py
import os

environment = os.environ.get("ENVIRONMENT", "production")

if environment == "development":
    BASE_URL = "https://npapi.propulsionhq.com/api/"
else:
    BASE_URL = "https://api.propulsionhq.com/api/"

# Dataset URLs
DATASET_UPDATE_URL = BASE_URL + "datasets/v1/dataset/{dataset_id}"
DATASET_UPLOAD_URL = BASE_URL + "datasets/v1/dataset/{dataset_id}/upload"
DATASET_IMPORT_URL = BASE_URL + "datasets/v1/dataset/{dataset_id}/import"
DATASET_CREATE_URL = BASE_URL + "datasets/v1/dataset"
