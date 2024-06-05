import datetime

import requests
from utils import interact_with_gpt
from logger import logger

def access_points(metadata):
    
    access_points = metadata['customFields']['Additional Information']['General Access Options']

    if not access_points:
            
            logger.warning('No access points available')
    
            return {'grade':'F', 'message':'No access points available', 'source_data': None}
    
    splitted_access_points = access_points.split(';')
    count_available_options = len(splitted_access_points)

    if count_available_options == 1:

        logger.info('Only one access point available')

        return {'grade':'C', 'message':'Only one access point available', 'source_data': access_points}
    
    elif count_available_options > 1 and count_available_options <= 3:

        logger.info('Up to 3 access points available')

        return {'grade':'B', 'message':'Up to 3 access points available', 'source_data': access_points}
    
    elif count_available_options > 3:
        
        logger.info('More than 3 access points available')

        return {'grade':'A', 'message':'More than 3 access points available', 'source_data': access_points}


def uri_availbalility(metadata):
    
    if metadata['dataUri']:

        logger.info('Data URI available')

        return {'grade':'A', 'message':'Data URI available', 'source_data': metadata['dataUri']}
    
    else:

        logger.warning('No Data URI available')

        return {'grade':'F', 'message':'No Data URI available', 'source_data': None}
    

def license_availability(metadata):
    
    if metadata['license']:

        logger.info('License available')

        return {'grade':'A', 'message':'License available', 'source_data': metadata['license']}
    
    else:

        logger.warning('No License available')

        return {'grade':'F', 'message':'No License available', 'source_data': None}


def metadata_updated_last_month(metadata):
    
    one_month_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
    two_months_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=60)
    three_months_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90)
    four_months_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=120)

    if metadata['metadataUpdatedAt']:

        try:

            metadata_updated_at = datetime.datetime.strptime(metadata['metadataUpdatedAt'], '%Y-%m-%dT%H:%M:%S%z')

        except ValueError:

            metadata_updated_at = datetime.datetime.strptime(metadata['metadataUpdatedAt'], '%Y-%m-%dT%H:%M:%S')
            metadata_updated_at = metadata_updated_at.replace(tzinfo=datetime.timezone.utc)

    else:

        metadata_updated_at = None

    if not metadata_updated_at:
         
        logger.warning('No metadata updated information available')

        return {'grade':'F', 'message':'No metadata updated information available', 'source_data': None}

    if metadata_updated_at > one_month_ago:

        logger.info('Metadata updated in the past month')

        return {'grade':'A', 'message':'Metadata updated in the past month', 'source_data': metadata['metadataUpdatedAt']}
    
    elif metadata_updated_at > two_months_ago and metadata_updated_at <= one_month_ago:

        logger.info('Metadata updated last month')

        return {'grade':'B', 'message':'Metadata updated last month', 'source_data': metadata['metadataUpdatedAt']}
    
    elif metadata_updated_at > three_months_ago and metadata_updated_at <= two_months_ago:

        logger.info('Metadata updated two months ago')

        return {'grade':'C', 'message':'Metadata updated two months ago', 'source_data': metadata['metadataUpdatedAt']}
    
    elif metadata_updated_at > four_months_ago and metadata_updated_at <= three_months_ago:

        logger.info('Metadata updated three months ago')

        return {'grade':'D', 'message':'Metadata updated three months ago', 'source_data': metadata['metadataUpdatedAt']}
    
    else:

        logger.warning('Metadata updated at least four months ago')

        return {'grade':'F', 'message':'Metadata updated at least four months ago', 'source_data': metadata['metadataUpdatedAt']}
    

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
    
    return {'grade': grade, 'message': explanation, 'source_data': description}


def category_availability(metadata):
    
    if metadata['category']:

        logger.info('Category available')

        return {'grade':'A', 'message':'Category available', 'source_data': metadata['category']}
    
    else:

        logger.warning('No Category available')

        return {'grade':'F', 'message':'No Category available', 'source_data': None}


def attribution_availability(metadata):

    if metadata['attribution']:

        logger.info('Attribution available')

        return {'grade':'A', 'message':'Attribution available', 'source_data': metadata['attribution']}
    
    else:

        logger.warning('No Attribution available')

        return {'grade':'F', 'message':'No Attribution available', 'source_data': None}

def financial_standards_applicable(metadata, data_sample):

    category = metadata['category']
    description = metadata['description']
    
    messages = [{"role": "system", "content": "You are an expert in financial data  with in-depth knowledge of the most important reporting standards, financial data regulations and fair data principles. Your expertise allows you to analyze financial datasets and metadata and determine which standards are applicable and whether the dataset adheres to these standards."},{"role": "user", "content": f"I have a dataset from finances.worldbank related to {category}. The dataset description is: {description}. Can you please: Identify which financial reporting standards could be applicable to this dataset? (OUTPUT PREFIX: POSSIBLE STANDARDS:) Evaluate if the dataset adheres to the identified standards. (OUTPUT PREFIX: ADHERENCE:) Assign a grade to the dataset based on its adherence to the standards, ranging from A to F (A being the best and F being the worst). (OUTPUT PREFIX: GRADE:) Here is a sample of the data: {data_sample}. Please provide a concise response."}]
    result = interact_with_gpt(messages=messages)

    result = result\
            .replace("OUTPUT","")\
            .replace("PREFIX","")\
            .replace("*","")
    
    possible_standards = result.split("STANDARDS:")[1].split("ADHERENCE:")[0].strip()
    adherence = result.split("ADHERENCE:")[1].split("GRADE:")[0].strip()
    grade = result.split("GRADE:")[1].strip()

    return {'grade': grade, 'possible_standards': possible_standards, 'adherence': adherence}

def identifier_accessible(metadata):
    
    if metadata['dataUri']:

        logger.info('Identifier available')
        
        response = requests.get(metadata['dataUri'])
        
        if response.status_code == 200:
            
            return {'grade':'A', 'message':'Identifier accessible', 'source_data': metadata['dataUri']}
        
        else:

            return {'grade':'F', 'message':'Identifier not accessible', 'source_data': None}
        
    else:

        logger.warning('No Identifier available')

        return {'grade':'F', 'message':'No Identifier available', 'source_data': None}
    
def check_metadata(metadata):
    
    if not metadata:
            
        logger.warning('No metadata available')
        
        return {'grade':'F', 'message':'No metadata programatically available', 'source_data': None}
    
    else:
        
        logger.info('Metadata available')

        return {'grade':'A', 'message':'Metadata programatically available', 'source_data': str(metadata)}
    
def check_audience(metadata):

    if metadata['approvals'][0]['targetAudience']:
        
        logger.info('Audience available')

        return {'grade':'A', 'message':'Audience available', 'source_data': metadata['approvals'][0]['targetAudience']}
    
    else:
            
        logger.warning('No Audience available')

        return {'grade':'F', 'message':'No Audience available', 'source_data': None}