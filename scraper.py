from bs4 import BeautifulSoup
import requests
import json

from mapper import map_to_unified_schema
from logger import logger

# Load the metadata element selectors
METADATA_ELEMENT_SELECTORS = json.load(open("elements.json"))


def scrape_metadata(url):
    """Scrape metadata from a given URL.

    Args:
        url (string): URL of a dataset.

    Returns:
        dict: Metadata of the dataset.
    """
    domain = url.split("https://")[1].split("/")[0]

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")
    
    # Get the metadata URL
    metadata_element = soup.select_one(METADATA_ELEMENT_SELECTORS[domain]["metadata_url"],href=True)
    logger.debug(f"Element containing metadata URL: {metadata_element}")

    # Get the metadata created at and updated at (This is needed for data.gov datasets, it can be skipped for other databases)
    metadata_created_at = soup.select_one(METADATA_ELEMENT_SELECTORS[domain]["metadata_created_at"]).text
    metadata_updated_at = soup.select_one(METADATA_ELEMENT_SELECTORS[domain]["metadata_updated_at"]).text

    # Get the metadata
    metadata_url = f"https://{domain}{metadata_element.get('href')}" #Building the metadata URL

    metadata = requests.get(metadata_url).json()

    metadata["createdAt"] = metadata_created_at
    metadata["metadataUpdatedAt"] = metadata_updated_at

    logger.info("Scraped Metadata.")
    logger.debug(f"Metadata scraped: {metadata}")

    return metadata


def scrape_dataset_csv(url):
    """Scrape the sample of a dataset

    Args:
        url (str): URL of the dataset

    Returns:
        str: Sample of the dataset (10 rows)
    """

    csv_content = "" # Default value of csv_content

    # Scrape the dataset
    try:

        domain = url.split("https://")[1].split("/")[0]

        html = requests.get(url).text

        soup = BeautifulSoup(html, "html.parser")

        # The part of the code below is to get the CSV URL and download the CSV file (this is specific to data.gov)
        csv_url_element = soup.select_one(METADATA_ELEMENT_SELECTORS[domain]["csv_url"]) # Get the CSV URL element
        csv_route_url = f"https://{domain}{csv_url_element.get('href')}"

        csv_html = requests.get(csv_route_url).text

        soup = BeautifulSoup(csv_html, "html.parser")

        csv_download_url_element = soup.select_one("a[href$='.csv']") # Get the CSV download URL element
        csv_download_url = csv_download_url_element.get("href") 
        
        # Download the CSV file and extract the first 10 rows
        csv_content = requests.get(csv_download_url).text
        
        csv_content = csv_content.split("\n")
        csv_content = str(csv_content[:10])

        logger.info("Scrape Sample Dataset.")
        logger.debug(f"Sample Dataset scraped: {csv_content}")
    
    except Exception as e:

        logger.info("No CSV found.")
        logger.debug(f"Error occured: {e}")

    return csv_content