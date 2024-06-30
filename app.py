from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from metrics import core_elements, provenance_check, uri_availbalility, id_availability, license_availability, check_data_accessible, check_data, description_analyzer, check_metadata, check_access_level, xbrl_standard_applicable, mci_standard_applicable, metadata_registries_standards_applicable
from api_handler import retrieve_metadata, retrieve_data_sample
from scraper import scrape_metadata, scrape_dataset_csv
from utils import calculate_summary_grade
import logging
from logger import logger
from mapper import map_to_unified_schema

# Set up logging
logging.basicConfig(level="INFO")

# Create the Flask app
app = Flask(__name__)
CORS(app) #Enable CORS for the app


def run_all_metrics(metadata, sample_data):

    uri_availbalility_result = uri_availbalility(metadata) #F1-01D Metric covered
    license_availability_result = license_availability(metadata) #R1.1-01M Metric covered
    description_analyzer_result = description_analyzer(metadata) #R1-01MD Metric covered
    xbrl_standard_applicable_result = xbrl_standard_applicable(metadata=metadata, data_sample=sample_data) #R1.3-01M Metric covered
    mci_standard_applicable_result = mci_standard_applicable(metadata=metadata, data_sample=sample_data) #R1.3-01M Metric covered
    metadata_registries_standards_applicable_result = metadata_registries_standards_applicable(metadata=metadata, data_sample=sample_data) #R1.3-01M Metric covered
    check_audience_result = check_access_level(metadata) #A1-01M Metric covered
    check_metadata_result = check_metadata(metadata) #F4-01M, A1-02M Metric covered
    data_accessible_result = check_data_accessible(data_sample=sample_data) #FA1-03D, R1.3-02D Metric covered
    core_elements_result = core_elements(metadata) #F2-01M Metric covered
    provenance_result = provenance_check(metadata) #R1.2-01M Metric covered
    data_csv_result = check_data(data_sample=sample_data) #R1.3-02D Metric covered
    id_availability_result = id_availability(metadata) #F1-02D Metric covered
    metadata_retention_period = {"grade":"F", "message":"No metadata retention period found.", "source_data":"", "subfix_element":"metadata_lifespan"} #A2-01M Metric covered, this has been manually examined for both databases and the information could not be found therefore the result is always F

    
    return {
        "metadata_availability_and_accessibility": check_metadata_result,
        "uri_availability": uri_availbalility_result,
        "license_availability": license_availability_result,
        "description_analyzer": description_analyzer_result,
        "check_audience": check_audience_result,
        "dataset_accessible": data_accessible_result,
        "core_elements": core_elements_result,
        "provenance_check": provenance_result,
        "dataset_available_in_standard_format": data_csv_result,
        "metadata_retention_period": metadata_retention_period,
        "xbrl_standard_applicable": xbrl_standard_applicable_result,
        "mci_standard_applicable": mci_standard_applicable_result,
        "metadata_registries_standards_applicable": metadata_registries_standards_applicable_result,
        "id_availability": id_availability_result   
    }

    
@app.route("/run_metrics", methods=["POST"])
def run_metrics():
    """Endpoint for the frontend to start running the metrics.

    Returns:
        dict: Results of the metrics.
    """

    data = request.json #Get the data of the request in json format
    
    logger.debug(f"Data received in /run_metrics: {data}")

    url = data.get("url") #Get the Dataset URL from the data

    if not url:

        logger.error("No URL provided")

        return jsonify({"error": "No URL provided"}), 400
    
    if "finances.worldbank.org" in url:

        uid = url.split("https://")[1].split("/")[3] #Get the unique identifier of the dataset from the URL

        metadata = retrieve_metadata(uid) #Retrieve the metadata of the dataset
        logger.debug(f"Metadata scraped from {url}: {metadata}")   
        
        sample_data = retrieve_data_sample(uid) #Retrieve the sample data of the dataset
        logger.debug(f"Sample data scraped from {url}: {sample_data}")
        
        metadata_unified = map_to_unified_schema(world_bank=metadata) #Map the metadata to a unified schema

    else:

        metadata = scrape_metadata(url) #Scrape the metadata of the dataset
        logger.debug(f"Metadata scraped from {url}: {metadata}")   

        sample_data = scrape_dataset_csv(url) #Scrape the sample data of the dataset
        logger.debug(f"Sample data scraped from {url}: {sample_data}")

        metadata_unified = map_to_unified_schema(data_gov=metadata) #Map the metadata to a unified schema

        
    metrics_results = run_all_metrics(metadata=metadata_unified, sample_data=sample_data) #Run all the metrics and get the results

    #Calculate summarized grade and add it to the results that are send back to the frontend
    summary_grade=calculate_summary_grade(metrics_results)
    metrics_results["summary_grade"]=summary_grade
    
    #Add the unified metadata and the provided URL to the results that are send back to the frontend
    additional_info = {
        "metadata": str(metadata_unified),
        "provided_url": url
    }
    metrics_results["additional_info"] = additional_info

    return jsonify(metrics_results)

@app.route("/")
def index():
    """Index page of the web application.
    """

    return render_template("index_webflow.html")

if __name__ == "__main__":
    app.run(debug=True)