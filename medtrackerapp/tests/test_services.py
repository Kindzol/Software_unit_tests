import unittest
from unittest.mock import patch, Mock
from medtrackerapp.models import DrugInfoService

class TestDrugInfoService(unittest.TestCase):

    @patch("medtrackerapp.services.requests.get")
    def test_fetch_drug_info(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = {
            "results": [{
                "openfda": {"generic_name": ["Ibuprofen"], "manufacturer_name": ["McKesson"]},
                "warnings": ["Keep out of reach of children."],
                "purpose": ["Pain reliever"]
            }]
        }
        result = DrugInfoService.get_drug_info("Ibuprofen")

        self.assertEqual(result["name"], "Ibuprofen")
        self.assertEqual(result["manufacturer"], "McKesson")
        self.assertEqual(result["warnings"], ["Keep out of reach of children."])
        self.assertEqual(result["purpose"], ["Pain reliever"])

    def test_drug_name_empty(self):
        with self.assertRaises(ValueError):
            DrugInfoService.get_drug_info("")

    @patch("medtrackerapp.services.requests.get")
    def test_api_non_200(self, mock_get):
        mock_get.return_value = Mock(status_code=500)
        with self.assertRaises(ValueError):
            DrugInfoService.get_drug_info("Ibuprofen")

    @patch("medtrackerapp.services.requests.get")
    def test_no_results_found(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = {"results": []}
        with self.assertRaises(ValueError):
            DrugInfoService.get_drug_info("Ibuprofen")