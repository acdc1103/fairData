import unittest
from unittest.mock import patch
import datetime
from metrics import access_points, check_audience, check_metadata, identifier_accessible, uri_availbalility, license_availability, metadata_updated_last_month, description_analyzer, category_availability, attribution_availability, financial_standards_applicable

class TestMetadataFunctions(unittest.TestCase):

    @patch('metrics.logger')
    def test_access_points(self, mock_logger):
        metadata_1 = {'customFields': {'Additional Information': {'General Access Options': 'Option1'}}}
        metadata_2 = {'customFields': {'Additional Information': {'General Access Options': 'Option1;Option2'}}}
        metadata_3 = {'customFields': {'Additional Information': {'General Access Options': 'Option1;Option2;Option3;Option4'}}}
        metadata_4 = {'customFields': {'Additional Information': {'General Access Options': None}}}

        self.assertEqual(access_points(metadata_1), {'grade': 'C', 'message': 'Only one access point available', 'source_data': 'Option1'})
        self.assertEqual(access_points(metadata_2), {'grade': 'B', 'message': 'Up to 3 access points available', 'source_data': 'Option1;Option2'})
        self.assertEqual(access_points(metadata_3), {'grade': 'A', 'message': 'More than 3 access points available', 'source_data': 'Option1;Option2;Option3;Option4'})
        self.assertEqual(access_points(metadata_4), {'grade': 'F', 'message': 'No access points available', 'source_data': None})

    @patch('metrics.logger')
    def test_uri_availbalility(self, mock_logger):
        metadata_1 = {'dataUri': 'http://example.com/data'}
        metadata_2 = {'dataUri': None}

        self.assertEqual(uri_availbalility(metadata_1), {'grade': 'A', 'message': 'Data URI available', 'source_data': 'http://example.com/data'})
        self.assertEqual(uri_availbalility(metadata_2), {'grade': 'F', 'message': 'No Data URI available', 'source_data': None})

    @patch('metrics.logger')
    def test_license_availability(self, mock_logger):
        metadata_1 = {'license': 'Creative Commons'}
        metadata_2 = {'license': None}

        self.assertEqual(license_availability(metadata_1), {'grade': 'A', 'message': 'License available', 'source_data': 'Creative Commons'})
        self.assertEqual(license_availability(metadata_2), {'grade': 'F', 'message': 'No License available', 'source_data': None})

    @patch('metrics.logger')
    def test_metadata_updated_last_month(self, mock_logger):
        now = datetime.datetime.now()
        metadata_1 = {'metadataUpdatedAt': (now - datetime.timedelta(days=10)).strftime('%Y-%m-%dT%H:%M:%SZ')}
        metadata_2 = {'metadataUpdatedAt': (now - datetime.timedelta(days=40)).strftime('%Y-%m-%dT%H:%M:%SZ')}
        metadata_3 = {'metadataUpdatedAt': (now - datetime.timedelta(days=70)).strftime('%Y-%m-%dT%H:%M:%SZ')}
        metadata_4 = {'metadataUpdatedAt': (now - datetime.timedelta(days=100)).strftime('%Y-%m-%dT%H:%M:%SZ')}
        metadata_5 = {'metadataUpdatedAt': (now - datetime.timedelta(days=130)).strftime('%Y-%m-%dT%H:%M:%SZ')}
        metadata_6 = {'metadataUpdatedAt': None}

        self.assertEqual(metadata_updated_last_month(metadata_1), {'grade': 'A', 'message': 'Metadata updated in the past month', 'source_data': metadata_1['metadataUpdatedAt']})
        self.assertEqual(metadata_updated_last_month(metadata_2), {'grade': 'B', 'message': 'Metadata updated last month', 'source_data': metadata_2['metadataUpdatedAt']})
        self.assertEqual(metadata_updated_last_month(metadata_3), {'grade': 'C', 'message': 'Metadata updated two months ago', 'source_data': metadata_3['metadataUpdatedAt']})
        self.assertEqual(metadata_updated_last_month(metadata_4), {'grade': 'D', 'message': 'Metadata updated three months ago', 'source_data': metadata_4['metadataUpdatedAt']})
        self.assertEqual(metadata_updated_last_month(metadata_5), {'grade': 'F', 'message': 'Metadata updated at least four months ago', 'source_data': metadata_5['metadataUpdatedAt']})
        self.assertEqual(metadata_updated_last_month(metadata_6), {'grade': 'F', 'message': 'No metadata updated information available', 'source_data': None})

    @patch('metrics.interact_with_gpt')
    def test_description_analyzer(self, mock_interact_with_gpt):
        mock_interact_with_gpt.return_value = 'GRADE: A EXPLANATION: The description is very detailed and informative.'
        metadata = {'description': 'This dataset contains comprehensive information about economic indicators.'}
        self.assertEqual(description_analyzer(metadata), {'grade': 'A', 'message': 'The description is very detailed and informative.', 'source_data': metadata['description']})

    @patch('metrics.logger')
    def test_category_availability(self, mock_logger):
        metadata_1 = {'category': 'Economics'}
        metadata_2 = {'category': None}

        self.assertEqual(category_availability(metadata_1), {'grade': 'A', 'message': 'Category available', 'source_data': 'Economics'})
        self.assertEqual(category_availability(metadata_2), {'grade': 'F', 'message': 'No Category available', 'source_data': None})

    @patch('metrics.logger')
    def test_attribution_availability(self, mock_logger):
        metadata_1 = {'attribution': 'World Bank'}
        metadata_2 = {'attribution': None}

        self.assertEqual(attribution_availability(metadata_1), {'grade': 'A', 'message': 'Attribution available', 'source_data': 'World Bank'})
        self.assertEqual(attribution_availability(metadata_2), {'grade': 'F', 'message': 'No Attribution available', 'source_data': None})

    @patch('metrics.interact_with_gpt')
    def test_financial_standards_applicable(self, mock_interact_with_gpt):
        mock_interact_with_gpt.return_value = 'POSSIBLE STANDARDS: IFRS ADHERENCE: Yes GRADE: A'
        metadata = {'category': 'Finance', 'description': 'Financial data on various metrics.'}
        data_sample = 'sample data content'
        self.assertEqual(financial_standards_applicable(metadata, data_sample), {'grade': 'A', 'possible_standards': 'IFRS', 'adherence': 'Yes'})
    
    def test_check_metadata(self):
        metadata_1 = {'dataUri': 'http://test.com'}
        metadata_2 = None
        self.assertEqual(check_metadata(metadata_1), {'grade': 'A', 'message': 'Metadata programatically available', 'source_data': str(metadata_1)})
        self.assertEqual(check_metadata(metadata_2), {'grade': 'F', 'message': 'No metadata programatically available', 'source_data': None})

    def test_check_audience(self):
        metadata_1 = {'approvals': [{'targetAudience': 'Public'}]}
        metadata_2 = {'approvals': [{'targetAudience': None}]}
        self.assertEqual(check_audience(metadata_1), {'grade': 'A', 'message': 'Audience available', 'source_data': 'Public'})
        self.assertEqual(check_audience(metadata_2), {'grade': 'F', 'message': 'No Audience available', 'source_data': None})

if __name__ == '__main__':
    unittest.main()