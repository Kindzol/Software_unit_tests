import unittest
from unittest.mock import patch, Mock
from medtrackerapp.models import DrugInfoService

class TestDrugInfoService(unittest.TestCase):

    @patch("medtrackerapp.models.requests.get")
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
