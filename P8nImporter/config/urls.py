# config/api_urls.py
BASE_URL = "https://api.propulsionhq.com/api/"
# BASE_URL = "http://localhost:3000/api/"

# Dataset URLs
DATASET_UPDATE_URL = BASE_URL + "datasets/v1/dataset/{dataset_id}"
DATASET_UPLOAD_URL = BASE_URL + "datasets/v1/dataset/{dataset_id}/upload"
DATASET_IMPORT_URL = BASE_URL + "datasets/v1/dataset/{dataset_id}/import"
DATASET_CREATE_URL = BASE_URL + "datasets/v1/dataset"