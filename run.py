import argparse
import logging

from api_handler import retrieve_metadata, retrieve_data_sample
from metrics import access_points, uri_availbalility, license_availability, metadata_updated_last_month, category_availability, attribution_availability, description_analyzer, financial_standards_applicable

parser = argparse.ArgumentParser(description='Set the logging level.')
parser.add_argument('--log', default='INFO', help='Set the logging level')

args = parser.parse_args()

numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f'Invalid log level: {args.log}')
logging.basicConfig(level=numeric_level)


metadata = retrieve_metadata('sfv5-tf7p')
sample_data = retrieve_data_sample('sfv5-tf7p')
print(metadata)
print(access_points(metadata))
llm_result = description_analyzer(metadata)
grade = llm_result\
        .split("GRADE: ")[1]\
        .split("EXPLANATION:")[0]\
        .strip()

print("GRADE:",grade)
explanation = llm_result\
        .split("EXPLANATION: ")[1]\
        .strip()

print("EXPLANATION:",explanation)

result = financial_standards_applicable(metadata, sample_data)
print("Result:",result)
