import requests
from logger import logger

def retrieve_metadata(dataset_uid):
    """Retrieve metadata from the World Bank API.

    Args:
        dataset_uid (str): The unique identifier of the dataset.

    Returns:
        dict: Metadata of the dataset.
    """
    # Construct the API URL
    metadata_url = f"https://finances.worldbank.org/api/views/metadata/v1/{dataset_uid}"

    # Make the API request
    response = requests.get(metadata_url)

    # Check if the request was successful
    if response.status_code == 200:
        metadata = response.json()
        logger.info('Successfully retrieved metadata')
        logger.debug(metadata)
        return metadata
    else:
        logger.error(f"Failed to retrieve metadata: {response.status_code}")
        logger.debug(f"Error message: {response.text}")
        return None


def retrieve_data_sample(dataset_uid):
    """Retrieve a sample of the data from the World Bank API.

    Args:
        dataset_uid (str): The unique identifier of the dataset.

    Returns:
        dict: Sample data of the dataset including 10 rows.
    """
    # Construct the API URL
    sample_data_url = f"https://finances.worldbank.org/resource/{dataset_uid}.json?$limit=10"

    # Make the API request
    response = requests.get(sample_data_url)

    # Check if the request was successful
    if response.status_code == 200:

        sample_data = response.json() #get sample data from response

        logger.info('Successfully retrieved metadata')
        logger.debug(sample_data)

        return sample_data
    
    else:

        logger.error(f"Failed to retrieve metadata: {response.status_code}")
        logger.debug(f"Error message: {response.text}")
        
        return None