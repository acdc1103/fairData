from bs4 import BeautifulSoup
import requests
import json

from mapper import map_to_unified_schema
from logger import logger

METADATA_ELEMENT_SELECTORS = json.load(open("elements.json"))


def scrape_metadata(url):

    domain = url.split("https://")[1].split("/")[0]

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")
        
    metadata_element = soup.select_one(METADATA_ELEMENT_SELECTORS[domain]['metadata_url'],href=True)
    print(metadata_element)
    metadata_created_at = soup.select_one(METADATA_ELEMENT_SELECTORS[domain]['metadata_created_at']).text
    metadata_updated_at = soup.select_one(METADATA_ELEMENT_SELECTORS[domain]['metadata_updated_at']).text

    metadata_url = f"https://{domain}{metadata_element.get('href')}"
    metadata = requests.get(metadata_url).json()
    metadata['createdAt'] = metadata_created_at
    metadata['metadataUpdatedAt'] = metadata_updated_at
    logger.info("Scrape Metadata.")
    return metadata

metadata = scrape_metadata("https://catalog.data.gov/dataset/fdic-failed-bank-list")

result = map_to_unified_schema(fdic=metadata, world_bank={})
print(result)

def scrape_dataset_csv(url):
    csv_content = ""
    try:
        domain = url.split("https://")[1].split("/")[0]

        html = requests.get(url).text

        soup = BeautifulSoup(html, "html.parser")

        csv_url_element = soup.select_one("a[title='Comma Separated Values File']")
        csv_route_url = f"https://{domain}{csv_url_element.get('href')}"

        csv_html = requests.get(csv_route_url).text

        soup = BeautifulSoup(csv_html, "html.parser")

        csv_download_url_element = soup.select_one("a[href$='.csv']")
        csv_download_url = csv_download_url_element.get('href') 
        
        csv_content = requests.get(csv_download_url).text
        csv_content = csv_content.split("\n")
        csv_content = str(csv_content[:10])
        logger.info("Scrape Sample Dataset.")
    except:
        logger.info("No CSV found.")
    return csv_content