import unittest
from unittest.mock import patch
from metrics import determine_grade, core_elements, uri_availbalility, id_availability, license_availability, description_analyzer, check_data_accessible, check_data, check_metadata, check_access_level, xbrl_standard_applicable

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.metadata = {
            "title": "Sample Dataset",
            "publisher": "Sample Publisher",
            "identifier": "http://example.com/dataset/123",
            "createdAt": "2020-01-01",
            "description": "This is a sample dataset for testing.",
            "keyword": "sample, test",
            "creator": "Sample Creator",
            "dataUri": "http://example.com/dataset/data",
            "license": "CC BY 4.0",
            "accessLevel": "public"
        }
        self.data_sample = "Sample data"

    def test_determine_grade(self):
        self.assertEqual(determine_grade(0.92), "A")
        self.assertEqual(determine_grade(0.49), "F")
        self.assertEqual(determine_grade(-1), "Invalid score")

    @patch('metrics.logger')
    def test_core_elements(self, mock_logger):
        result = core_elements(self.metadata)
        print(result)
        self.assertEqual(result["grade"], "A")
        self.assertIn("Title available", result["message"])

    @patch('metrics.logger')
    def test_uri_availability(self, mock_logger):
        result = uri_availbalility(self.metadata)
        self.assertEqual(result["grade"], "A")
        self.assertIn("Data URI available", result["message"])

    @patch('metrics.logger')
    def test_id_availability(self, mock_logger):
        result = id_availability(self.metadata)
        self.assertEqual(result["grade"], "F")
        self.assertIn("ID available", result["message"])

    @patch('metrics.logger')
    def test_license_availability(self, mock_logger):
        result = license_availability(self.metadata)
        self.assertEqual(result["grade"], "A")
        self.assertIn("License available", result["message"])

    @patch('metrics.logger')
    def test_check_data_accessible(self, mock_logger):
        result = check_data_accessible(self.data_sample)
        self.assertEqual(result["grade"], "A")
        self.assertIn("Data accessible", result["message"])

    @patch('metrics.logger')
    def test_check_data(self, mock_logger):
        result = check_data(self.data_sample)
        self.assertEqual(result["grade"], "A")
        self.assertIn("Data available in standard formats", result["message"])

    @patch('metrics.logger')
    def test_check_metadata(self, mock_logger):
        result = check_metadata(self.metadata)
        self.assertEqual(result["grade"], "A")
        self.assertIn("Metadata programatically available", result["message"])

    @patch('metrics.logger')
    def test_check_access_level(self, mock_logger):
        result = check_access_level(self.metadata)
        self.assertEqual(result["grade"], "A")
        self.assertIn("Access Level available", result["message"])

    # Mocking external interactions for description_analyzer and xbrl_standard_applicable is necessary
    # These would involve patching the external interaction methods and providing return values that simulate expected responses.

if __name__ == '__main__':
    unittest.main()