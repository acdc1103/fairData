from utils import interact_with_gpt, standards_gpt_workflow, determine_grade
from logger import logger
import re

#All these metrics return almost the same dictionary with the grade, message, source data (optional) and subfix element. The subfix element is important for the frontend to know where to display the results.

def core_elements(metadata):
    """Metric that checks the core elements of a metadata.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    logger.info("Checking core elements of metadata")

    #Setting default values for variables
    score = 0
    max_score = 7
    message = ""
    source_data = ""
    
    #Checking if title is available
    if metadata.get("title"):
        score += 1
        message += "Title available \n"
        source_data += f"Title: {metadata['title']}\n"

    #Checking if publisher is available   
    if metadata.get("publisher"):  
        score += 1
        message += "Publisher available \n"
        source_data += f"Publisher: {metadata['publisher']}\n"

    #Checking if identifier is available
    if metadata.get("identifier"):
        score += 1
        message += "Identifier available \n"
        source_data += f"Identifier: {metadata['identifier']}\n"

    #Checking if createdAt is available
    if metadata.get("createdAt"):
        score += 1
        message += "Created at available \n"
        source_data += f"Created at: {metadata['createdAt']}\n"

    #Checking if metadataUpdatedAt is available
    if metadata.get("description"):
        score += 1
        message += "Description available \n"
        source_data += f"Description: {metadata['description']}\n"

    #Checking if keyword is available
    if metadata.get("keyword"):
        score += 1
        message += "Keyword available \n"
        source_data += f"Keyword: {metadata['keyword']}\n"

    #Checking if creator is available
    if metadata.get("creator"):
        score += 1
        message += "Creator available \n"
        source_data += f"Creator: {metadata['creator']}\n"

    #Calculating the grade based on the average score
    grade = round(score / max_score,2)
    return {"grade": determine_grade(grade), "message": message, "source_data": source_data, "subfix_element": "core_elements"}


def uri_availbalility(metadata):
    """Metric that checks the availability of a data URI in the metadata.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    if metadata.get("dataUri", None):
        
        logger.info("Data URI available")

        return {"grade":"A", "message":"Data URI available", "source_data": metadata['dataUri'], "subfix_element":"uri"}
    
    else:

        logger.warning("No Data URI available")

        return {"grade":"F", "message":"No Data URI available", "source_data": None, "subfix_element":"uri"}
    

def id_availability(metadata):
    """Metric that checks the availability of an identifier in the metadata.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    if metadata.get("identifier"):
        
        pattern = re.compile(r"^(https?://)")

        if pattern.match(metadata.get("identifier")) is not None:
            logger.info("ID available")
            return {"grade":"F", "message":"No ID available", "source_data": metadata['identifier'], "subfix_element":"unique_id"}
        
        return {"grade":"A", "message":"ID available", "source_data": metadata['identifier'], "subfix_element":"unique_id"}
    
    else:

        logger.warning("No ID available")

        return {"grade":"F", "message":"No ID available", "source_data": None, "subfix_element":"unique_id"}


def license_availability(metadata):
    """Metric that checks the availability of a license in the metadata.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    if metadata.get("license", None):

        logger.info("License available")

        return {"grade":"A", "message":"License available", "source_data": metadata['license'], "subfix_element":"license"}
    
    else:

        logger.warning("No License available")

        return {"grade":"F", "message":"No License available", "source_data": None, "subfix_element":"license"}
    

def description_analyzer(metadata):
    """Metric that checks the quality of the description in the metadata.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    description = metadata['description']

    messages = [{"role": "system", 
                 "content": "You are a open data analyzer and analyze metadata of datasets based on the FAIR Data framework."},
                {"role": "user", 
                 "content": f"""Do you think this description of the dataset is accurate enough and explains the dataset good. 
                 Please give me a grade from A to F (A is the best and F the worst). 
                 Only output A, B, C, D or F for the grading with prefix GRADE: including the explaination with a prefix EXPLANATION: why you gave that certain grade  
                 and don"t do any text formatting. Here is the dataset description: {description}"""}
                ]
    
    grading = interact_with_gpt(messages=messages) #Sending the message to ChatGPT

    #Extracting the grade and explanation from the response
    grade = grading\
        .split("GRADE: ")[1]\
        .split("EXPLANATION:")[0]\
        .strip()
    logger.debug(f"Description GRADE: {grade}")

    explanation = grading\
            .split("EXPLANATION: ")[1]\
            .strip()
    logger.debug(f"Description EXPLANATION: {explanation}")

    return {"grade": grade, "message": explanation, "source_data": description, "subfix_element":"description"}


def check_data_accessible(data_sample):
    """Metric that checks if data is accessible.

    Args:
        data_sample (str): Sample of the dataset containing 10 rows.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    if not data_sample:
            
        logger.warning("No Data accessible")
        
        return {"grade":"F", "message":"No Data accessible", "source_data": None, "subfix_element":"dataset_access"}
    
    else:
        
        logger.info("Data Sample available")

        return {"grade":"A", "message":"Data accessible", "source_data": "Output too big.", "subfix_element":"dataset_access"}



def check_data(data_sample):
    """Checks if data is available in standard formats (CSV, JSON, XML, etc.).

    Args:
        data_sample (str): Sample of the dataset containing 10 rows.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """
    if not data_sample:
        
        logger.warning("No Data available in standard formats (CSV, JSON, XML, etc.)")
        
        return {"grade":"F", "message":"No Data in standard formats available", "source_data": None, "subfix_element":"dataset_csv"}
    
    else:
        
        logger.info("Data Sample available")

        return {"grade":"A", "message":"Data available in standard formats (CSV, JSON, XML,  HTML, etc.)", "source_data": "Output too big.", "subfix_element":"dataset_csv"}


def check_metadata(metadata):
    """Metric that checks if metadata is programatically available.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    if not metadata:
            
        logger.warning("No metadata available")
        
        return {"grade":"F", "message":"No metadata machine readable available", "source_data": None, "subfix_element":"metadata"}
    
    else:
        
        logger.info("Metadata available")

        return {"grade":"A", "message":"Metadata programatically available", "source_data": str(metadata), "subfix_element":"metadata"}
    

def check_access_level(metadata):
    """Metric that checks if access level is available in the metadata.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    if metadata.get("accessLevel", None):
        
        logger.info("Access Level available")

        return {"grade":"A", "message":"Access Level available", "source_data": metadata['accessLevel'], "subfix_element":"access_level"}
    
    else:
            
        logger.warning("No Access Level available")

        return {"grade":"F", "message":"No Access Level available", "source_data": None, "subfix_element":"access_level"}
    

def xbrl_standard_applicable(metadata, data_sample):
    """Checks if the XBRL standard is applicable to the dataset.
    
    Args:
        metadata (dict): Metadata of a dataset.
        data_sample (str): Sample of the dataset containing 10 rows.

    Returns:
        dict: Dictionary with results of the metric including grade, message, and subfix element.
    """

    messages = [{"role": "system", 
                 "content": """You are an expert in meta data  with in-depth knowledge of the XBRL GAAP Taxonomy standards. 
                 Your expertise allows you to analyze datasets and metadata and determine if the standard is applicable and whether the dataset adheres to this standard."""},
                 {"role": "user", 
                  "content": f"""I have a dataset with following metadata: {metadata}.  
                  Can you please: Identify if XBRL standard could be applicable to this dataset and Evaluate if the dataset adheres to the identified standards (OUTPUT PREFIX: ADHERENCE:). 
                  Assign a grade to the dataset based on its adherence to the standards, ranging from A to F (A being the best and F being the worst) (OUTPUT PREFIX: GRADE:). 
                  Here is a sample of the data: {data_sample}. Please provide a concise response according to the output prefixes.
                  If it does not fall under the purview of XBRL GAAP standards than respond with "GRADE: not applicable ADHERENCE: not applicable POSSIBLE STANDARDS: not applicable"""}
                ]
    
    #Interacting with GPT-4o to get results
    results = standards_gpt_workflow(messages)
    results["subfix_element"] = "xbrl"

    logger.debug(f"Results of standards evaluation: {results}")

    return results


def mci_standard_applicable(metadata, data_sample):
    """Checks if the MCI standard is applicable to the dataset.
    
    Args:
        metadata (dict): Metadata of a dataset.
        data_sample (str): Sample of the dataset containing 10 rows.

    Returns:
        dict: Dictionary with results of the metric including grade, message, and subfix element.
    """

    messages = [{"role": "system", 
                 "content": """You are an expert in meta data  with in-depth knowledge of the Metadata Coverage Index (MCI) standards. 
                 Your expertise allows you to analyze datasets and metadata and determine if the standard is applicable and whether the dataset adheres to this standard."""},
                 {"role": "user", 
                  "content": f"""I have a dataset with following metadata: {metadata}.  
                  Can you please: Identify if Metadata Coverage Index (MCI) standard could be applicable to this dataset and  
                  Evaluate if the dataset adheres to the identified standards (OUTPUT PREFIX: ADHERENCE:). 
                  Assign a grade to the dataset based on its adherence to the standards, ranging from A to F (A being the best and F being the worst) (OUTPUT PREFIX: GRADE:). 
                  Here is a sample of the data: {data_sample}. Please provide a concise response according to the output prefixes."""}
                ]
    
    #Interacting with GPT-4o to get results
    results = standards_gpt_workflow(messages)
    results["subfix_element"] = "mci"

    logger.debug(f"Results of standards evaluation: {results}")
    
    return results


def metadata_registries_standards_applicable(metadata, data_sample):
    """Checks if the Metadata Registers standard is applicable to the dataset.
    
    Args:
        metadata (dict): Metadata of a dataset.
        data_sample (str): Sample of the dataset containing 10 rows.

    Returns:
        dict: Dictionary with results of the metric including grade, message, and subfix element.
    """

    messages = [{"role": "system", 
                 "content": """You are an expert in meta data  with in-depth knowledge of the ISO/IEC 11179 - Metadata Registries standards . 
                 Your expertise allows you to analyze datasets and metadata and determine if the standard is applicable and whether the dataset adheres to this standard."""},
                 {"role": "user", 
                  "content": f"""I have a dataset with following metadata: {metadata}.  
                  Can you please: Identify if ISO/IEC 11179 - Metadata Registries standards could be applicable to this dataset and
                  Evaluate if the dataset adheres to the identified standards (OUTPUT PREFIX: ADHERENCE:). 
                  Assign a grade to the dataset based on its adherence to the standards, ranging from A to F (A being the best and F being the worst) (OUTPUT PREFIX: GRADE:). 
                  Here is a sample of the data: {data_sample}. Please provide a concise response according to the output prefixes."""}
                ]
    
    
    
    #Interacting with GPT-4o to get results
    results = standards_gpt_workflow(messages)
    results["subfix_element"] = "metadata_registers"

    logger.debug(f"Results of standards evaluation: {results}")
    
    return results


def provenance_check(metadata):
    """Checks the provenance of the metadata.

    Args:
        metadata (dict): Metadata of a dataset.

    Returns:
        dict: Dictionary with results of the metric including grade, message, source data (data the metric was tested on) and subfix element.
    """

    #Setting default values for variables
    score = 0
    max_score = 5
    message = ""
    source_data = ""
    
    #Checking if publisher is available
    if metadata.get("publisher"):  
        score += 1
        message += "Publisher available \n"
        source_data += f"Publisher: {metadata['publisher']}\n"

    #Checking if createdAt is available
    if metadata.get("createdAt"):
        score += 1
        message += "Created at available \n"
        source_data += f"Created at: {metadata['createdAt']}\n"

    #Checking if contributor is available
    if metadata.get("contributor"):
        score += 1
        message += "Contributor available \n"
        source_data += f"Contributor: {metadata['contributor']}\n"

    #Checking if metadataUpdatedAt is available
    if metadata.get("metadataUpdatedAt"):
        score += 1
        message += "Metadata Updated at available \n"
        source_data += f"Metadata Updated at: {metadata['metadataUpdatedAt']}\n"

    #Checking if creator is available
    if metadata.get("creator"):
        score += 1
        message += "Creator available \n"
        source_data += f"Creator: {metadata['creator']}\n"
    
    #Calculating the grade based on the average score
    grade = score / max_score

    return {"grade":determine_grade(grade), "message": message, "source_data": source_data, "subfix_element":"provenance"}