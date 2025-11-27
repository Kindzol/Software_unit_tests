from rest_framework.test import APITestCase
from medtrackerapp.models import Medication, DoseLog
from django.urls import reverse
from rest_framework import status


class MedicationViewTests(APITestCase):
    def setUp(self):
        self.med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)

# list
    def test_list_medications_valid_data(self):
        url = reverse("medication-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Aspirin")
        self.assertEqual(response.data[0]["dosage_mg"], 100)

# create
    def test_create_medication_valid_data(self):
        url = reverse("medication-list")
        data = {
            "name": "Aspirin",
            "dosage_mg": 200,
            "prescribed_per_day": 3
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medication.objects.count(), 2)
        self.assertEqual(Medication.objects.get(id=response.data["id"]).name, "Aspirin")

    def test_create_medication_invalid_data(self):
        url = reverse("medication-list")
        data = {
            "name": "",  #name is required
            "dosage_mg": -50,  #dosage must be positive
            "prescribed_per_day": 0  # must be at least 1
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("dosage_mg", response.data)
        self.assertNotIn("prescribed_per_day", response.data)


# retrieve
    def test_retrieve_medication_valid_id(self):
        url = reverse("medication-detail", args=[self.med.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Aspirin")
        self.assertEqual(response.data["dosage_mg"], 100)

    def test_retrieve_medication_invalid_id(self):
        url = reverse("medication-detail", args=[999])  #non-existent ID
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# update
    def test_update_medication_valid_data(self):
        url = reverse("medication-detail", args=[self.med.id])
        data = {
            "name": "Updated Aspirin",
            "dosage_mg": 150,
            "prescribed_per_day": 4
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.med.refresh_from_db()
        self.assertEqual(self.med.name, "Updated Aspirin")
        self.assertEqual(self.med.dosage_mg, 150)
        self.assertEqual(self.med.prescribed_per_day, 4)

    def test_update_medication_invalid_data(self):
        url = reverse("medication-detail", args=[self.med.id])
        data = {
            "name": "",  #name is required
            "dosage_mg": -100,  #must be positive
            "prescribed_per_day": 0  #must be at least 1
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("dosage_mg", response.data)
        self.assertNotIn("prescribed_per_day", response.data)

# delete
    def test_delete_medication_valid_id(self):
        url = reverse("medication-detail", args=[self.med.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Medication.objects.count(), 0)

    def test_delete_medication_invalid_id(self):
        url = reverse("medication-detail", args=[999])  #non-existent ID
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class DoseLogViewTests(APITestCase):
    def setUp(self):
        self.med = Medication.objects.create(name="Ibuprofen", dosage_mg=200, prescribed_per_day=3)
        self.log = DoseLog.objects.create(
            medication=self.med,
            taken_at="2025-12-01T08:00:00Z",
            was_taken=True
        )

# list
    def test_list_doselogs(self):
        url = reverse("doselog-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

# create
    def test_create_doselog_valid_data(self):
        url = reverse("doselog-list")
        data = {
            "medication": self.med.id,
            "taken_at": "2025-12-01T08:00:00Z",
            "was_taken": True
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["medication"], self.med.id)
        self.assertEqual(response.data["was_taken"], True)

    def test_create_doselog_invalid_data(self):
        url = reverse("doselog-list")
        data = {"medication": None,
                "taken_at": "bad-date",
                "was_taken": True}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("medication", response.data)
        self.assertIn("taken_at", response.data)
        self.assertNotIn("was_taken", response.data)

# retrieve
    def test_retrieve_doselog_valid_id(self):
        url = reverse("doselog-detail", args=[self.log.id])  # <-- self.log.id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["medication"], self.med.id)

    def test_retrieve_doselog_invalid_id(self):
        url = reverse("doselog-detail", args=[999])  #non-existent ID
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# update
    def test_update_doselog_valid_data(self):
        url = reverse("doselog-detail", args=[self.log.id])  # <-- self.log.id
        data = {
            "medication": self.med.id,
            "taken_at": "2025-12-01T09:00:00Z",
            "was_taken": False
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["was_taken"], False)

    def test_update_doselog_invalid_data(self):
        url = reverse("doselog-detail", args=[self.log.id])  # <-- self.log.id
        data = {
            "medication": None,
            "taken_at": "invalid-date",
            "was_taken": "not-a-boolean"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("medication", response.data)
        self.assertIn("taken_at", response.data)
        self.assertIn("was_taken", response.data)

# delete
    def test_delete_doselog_valid_id(self):
        url = reverse("doselog-detail", args=[self.log.id])  # <-- self.log.id
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DoseLog.objects.count(), 0)

    def test_delete_doselog_invalid_id(self):
        url = reverse("doselog-detail", args=[999])  #non-existent ID
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
