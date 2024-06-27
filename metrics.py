from utils import interact_with_gpt
from logger import logger
import re

GRADING_SYSTEM = [
    ("A", 0.9, 1.0),
    ("B", 0.8, 0.9),
    ("C", 0.7, 0.8),
    ("D", 0.6, 0.7),
    ("E", 0.5, 0.6),
    ("F", 0.0, 0.5),
]

def determine_grade(score):
    for grade, lower_bound, upper_bound in GRADING_SYSTEM:
        if lower_bound <= score < upper_bound:
            return grade
    return "Invalid score"


def core_elements(metadata):
    
    score = 0
    max_score = 7
    message = ''
    source_data = ''
    
    if metadata.get('title'):
        score += 1
        message += 'Title available \n'
        source_data += f"Title: {metadata['title']}\n"
        
    if metadata.get('publisher'):  
        score += 1
        message += 'Publisher available \n'
        source_data += f"Publisher: {metadata['publisher']}\n"

    if metadata.get('identifier'):
        score += 1
        message += 'Identifier available \n'
        source_data += f"Identifier: {metadata['identifier']}\n"

    if metadata.get('createdAt'):
        score += 1
        message += 'Created at available \n'
        source_data += f"Created at: {metadata['createdAt']}\n"

    if metadata.get('description'):
        score += 1
        message += 'Description available \n'
        source_data += f"Description: {metadata['description']}\n"

    if metadata.get('keyword'):
        score += 1
        message += 'Keyword available \n'
        source_data += f"Keyword: {metadata['keyword']}\n"

    if metadata.get('creator'):
        score += 1
        message += 'Creator available \n'
        source_data += f"Creator: {metadata['creator']}\n"

    grade = score / max_score

    return {'grade':determine_grade(grade), 'message': message, 'source_data': source_data, 'subfix_element': 'core_elements'}


def uri_availbalility(metadata):

    if metadata.get('dataUri', None):
        
        logger.info('Data URI available')

        return {'grade':'A', 'message':'Data URI available', 'source_data': metadata['dataUri'], 'subfix_element':'uri'}
    
    else:

        logger.warning('No Data URI available')

        return {'grade':'F', 'message':'No Data URI available', 'source_data': None, 'subfix_element':'uri'}
    

def id_availability(metadata):
    
    if metadata.get('identifier'):
        
        pattern = re.compile(r'^(https?://)')
        if pattern.match(metadata.get('identifier')) is not None:
            return {'grade':'F', 'message':'No ID available', 'source_data': metadata['identifier'], 'subfix_element':'unique_id'}
        
        return {'grade':'A', 'message':'ID available', 'source_data': metadata['identifier'], 'subfix_element':'unique_id'}
    else:
        return {'grade':'F', 'message':'No ID available', 'source_data': None, 'subfix_element':'unique_id'}


def license_availability(metadata):
    
    if metadata.get('license', None):

        logger.info('License available')

        return {'grade':'A', 'message':'License available', 'source_data': metadata['license'], 'subfix_element':'license'}
    
    else:

        logger.warning('No License available')

        return {'grade':'F', 'message':'No License available', 'source_data': None, 'subfix_element':'license'}
    

def description_analyzer(metadata):
    
    description = metadata['description']

    messages = [{"role": "system", "content": "You are a open data analyzer and analyze metadata of datasets based on the FAIR Data framework."},{"role": "user", "content": f"Do you think this description of the dataset is accurate enough and explains the dataset good. please give me a grade from A to F (A is the best and F the worst). Only output A, B, C, D or F for the grading with prefix GRADE: including the explaination with a prefix EXPLANATION: why you gave that certain grade  and don't do any text formatting. Here is the dataset description: {description}"}]
    grading = interact_with_gpt(messages=messages)

    grade = grading\
        .split("GRADE: ")[1]\
        .split("EXPLANATION:")[0]\
        .strip()

    print("GRADE:",grade)
    explanation = grading\
            .split("EXPLANATION: ")[1]\
            .strip()
    
    return {'grade': grade, 'message': explanation, 'source_data': description, 'subfix_element':'description'}


def check_data_accessible(data_sample):
    
    if not data_sample:
            
        logger.warning('No Data accessible')
        
        return {'grade':'F', 'message':'No Data accessible', 'source_data': None, 'subfix_element':'dataset_access'}
    
    else:
        
        logger.info('Data Sample available')

        return {'grade':'A', 'message':'Data accessible', 'source_data': 'Output too big.', 'subfix_element':'dataset_access'}



def check_data(data_sample):
    
    if not data_sample:
            
        logger.warning('No Data available in standard formats (CSV, JSON, XML, etc.)')
        
        return {'grade':'F', 'message':'No Data in standard formats available', 'source_data': None, 'subfix_element':'dataset_csv'}
    
    else:
        
        logger.info('Data Sample available')

        return {'grade':'A', 'message':'Data available in standard formats (CSV, JSON, XML,  HTML, etc.)', 'source_data': 'Output too big.', 'subfix_element':'dataset_csv'}


def check_metadata(metadata):
    
    if not metadata:
            
        logger.warning('No metadata available')
        
        return {'grade':'F', 'message':'No metadata machine readable available', 'source_data': None, 'subfix_element':'metadata'}
    
    else:
        
        logger.info('Metadata available')

        return {'grade':'A', 'message':'Metadata programatically available', 'source_data': str(metadata), 'subfix_element':'metadata'}
    

def check_access_level(metadata):

    if metadata.get('accessLevel', None):
        
        logger.info('Access Level available')

        return {'grade':'A', 'message':'Access Level available', 'source_data': metadata['accessLevel'], 'subfix_element':'access_level'}
    
    else:
            
        logger.warning('No Access Level available')

        return {'grade':'F', 'message':'No Access Level available', 'source_data': None, 'subfix_element':'access_level'}
    

def xbrl_standard_applicable(metadata, data_sample):
        
    messages = [{"role": "system", "content": """You are an expert in meta data  with in-depth knowledge of the XBRL GAAP Taxonomy standards. 
                 Your expertise allows you to analyze datasets and metadata and determine if the standard is applicable and whether the dataset adheres to this standard."""},
                 {"role": "user", "content": f"""I have a dataset with following metadata: {metadata}.  
                  Can you please: Identify if XBRL standard could be applicable to this dataset? (OUTPUT PREFIX: POSSIBLE STANDARDS:). 
                  Evaluate if the dataset adheres to the identified standards (OUTPUT PREFIX: ADHERENCE:). 
                  Assign a grade to the dataset based on its adherence to the standards, ranging from A to F (A being the best and F being the worst) (OUTPUT PREFIX: GRADE:). 
                  Here is a sample of the data: {data_sample}. Please provide a concise response according to the output prefixes.
                 If it does not fall under the purview of XBRL GAAP standards than respond with 'GRADE: not applicable ADHERENCE: not applicable POSSIBLE STANDARDS: not applicable'"""}]
    result = interact_with_gpt(messages=messages)

    result = result\
            .replace("OUTPUT","")\
            .replace("PREFIX","")\
            .replace("*","")
    
    possible_standards = result.split("STANDARDS:")[1].split("ADHERENCE:")[0].strip()
    adherence = result.split("ADHERENCE:")[1].split("GRADE:")[0].strip()
    grade = result.split("GRADE:")[1].strip()
    grade = grade[0]
    if grade == 'n':
        grade = 'not applicable'

    return {'grade': grade, 'message': adherence, 'subfix_element':'xbrl'}


def mci_standard_applicable(metadata, data_sample):
        
    messages = [{"role": "system", "content": """You are an expert in meta data  with in-depth knowledge of the Metadata Coverage Index (MCI) standards. 
                 Your expertise allows you to analyze datasets and metadata and determine if the standard is applicable and whether the dataset adheres to this standard."""},
                 {"role": "user", "content": f"""I have a dataset with following metadata: {metadata}.  
                  Can you please: Identify if Metadata Coverage Index (MCI) standard could be applicable to this dataset? (OUTPUT PREFIX: POSSIBLE STANDARDS:). 
                  Evaluate if the dataset adheres to the identified standards (OUTPUT PREFIX: ADHERENCE:). 
                  Assign a grade to the dataset based on its adherence to the standards, ranging from A to F (A being the best and F being the worst) (OUTPUT PREFIX: GRADE:). 
                  Here is a sample of the data: {data_sample}. Please provide a concise response according to the output prefixes."""}]
    result = interact_with_gpt(messages=messages)

    result = result\
            .replace("OUTPUT","")\
            .replace("PREFIX","")\
            .replace("*","")
    
    possible_standards = result.split("STANDARDS:")[1].split("ADHERENCE:")[0].strip()
    adherence = result.split("ADHERENCE:")[1].split("GRADE:")[0].strip()
    grade = result.split("GRADE:")[1].strip()
    grade = grade[0]

    return {'grade': grade, 'message': adherence, 'subfix_element':'mci'}


def metadata_registries_standards_applicable(metadata, data_sample):
    
    messages = [{"role": "system", "content": """You are an expert in meta data  with in-depth knowledge of the ISO/IEC 11179 - Metadata Registries standards . 
                 Your expertise allows you to analyze datasets and metadata and determine if the standard is applicable and whether the dataset adheres to this standard."""},
                 {"role": "user", "content": f"""I have a dataset with following metadata: {metadata}.  
                  Can you please: Identify if ISO/IEC 11179 - Metadata Registries standards could be applicable to this dataset? (OUTPUT PREFIX: POSSIBLE STANDARDS:). 
                  Evaluate if the dataset adheres to the identified standards (OUTPUT PREFIX: ADHERENCE:). 
                  Assign a grade to the dataset based on its adherence to the standards, ranging from A to F (A being the best and F being the worst) (OUTPUT PREFIX: GRADE:). 
                  Here is a sample of the data: {data_sample}. Please provide a concise response according to the output prefixes."""}]
    result = interact_with_gpt(messages=messages)

    result = result\
            .replace("OUTPUT","")\
            .replace("PREFIX","")\
            .replace("*","")
    
    possible_standards = result.split("STANDARDS:")[1].split("ADHERENCE:")[0].strip()
    adherence = result.split("ADHERENCE:")[1].split("GRADE:")[0].strip()
    grade = result.split("GRADE:")[1].strip()
    grade = grade[0]
    return {'grade': grade, 'message': adherence, 'subfix_element':'metadata_registers'}


def provenance_check(metadata):
    
    score = 0
    max_score = 5
    message = ''
    source_data = ''
    
    if metadata.get('publisher'):  
        score += 1
        message += 'Publisher available \n'
        source_data += f"Publisher: {metadata['publisher']}\n"

    if metadata.get('createdAt'):
        score += 1
        message += 'Created at available \n'
        source_data += f"Created at: {metadata['createdAt']}\n"

    if metadata.get('contributor'):
        score += 1
        message += 'Contributor available \n'
        source_data += f"Contributor: {metadata['contributor']}\n"

    if metadata.get('metadataUpdatedAt'):
        score += 1
        message += 'Metadata Updated at available \n'
        source_data += f"Metadata Updated at: {metadata['metadataUpdatedAt']}\n"

    if metadata.get('creator'):
        score += 1
        message += 'Creator available \n'
        source_data += f"Creator: {metadata['creator']}\n"

    grade = score / max_score

    return {'grade':determine_grade(grade), 'message': message, 'source_data': source_data, 'subfix_element':'provenance'}