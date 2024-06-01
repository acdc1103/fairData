import requests
from logger import logger

def retrieve_metadata(dataset_uid):

    # Construct the API URL
    metadata_url = f"https://finances.worldbank.org/api/views/metadata/v1/{dataset_uid}"

    # Make the API request
    response = requests.get(metadata_url)

    # Check if the request was successful
    if response.status_code == 200:
        metadata = response.json()
        logger.info('Successfully retrieved metadata')
        return metadata
    else:
        logger.error(f"Failed to retrieve metadata: {response.status_code}")
        logger.debug(f"Error message: {response.text}")
        return None


def retrieve_data_sample(dataset_uid):

    # Construct the API URL
    sample_data_url = f"https://finances.worldbank.org/resource/{dataset_uid}.json?$limit=10"

    # Make the API request
    response = requests.get(sample_data_url)

    # Check if the request was successful
    if response.status_code == 200:
        sample_data = response.json()
        logger.info('Successfully retrieved metadata')
        return sample_data
    else:
        logger.error(f"Failed to retrieve metadata: {response.status_code}")
        logger.debug(f"Error message: {response.text}")
        return None