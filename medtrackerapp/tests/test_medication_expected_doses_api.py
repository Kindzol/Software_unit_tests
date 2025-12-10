from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from medtrackerapp.models import Medication


class MedicationExpectedDosesTest(APITestCase):

    def setUp(self):
        self.medication = Medication.objects.create(
            name="Aspirin",
            dosage_mg=500,
            prescribed_per_day=2
        )
        self.url = reverse("medication-expected-doses", args=[self.medication.id])

    def test_expected_doses_valid(self,url):
        response = self.client.get(url, {'days': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['medication_id'], self.medication.id)
        self.assertEqual(response.data['days'], 2)
        self.assertEqual(response.data['expected_doses'], 10)


    def test_expected_doses_invalid_days(self, url):
        response = self.client.get(url, {'days': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expected_doses_missing_days(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

