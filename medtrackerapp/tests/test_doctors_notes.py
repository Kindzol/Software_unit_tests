from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from medtrackerapp.models import Medication, DoctorsNote

class DoctorsNotesTest(APITestCase):
    def setUp(self):
        self.medication = Medication.objects.create(
            name="Aspirin",
            dosage_mg=500,
            prescribed_per_day=2
        )
        # Correct URL name for the list endpoint
        self.url = reverse("doctors_notes-list")

    def test_create_note_valid(self):
        data = {
            "medication": self.medication.id,
            "content": "Patient is responding well to the medication."
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['medication'], self.medication.id)
        self.assertEqual(response.data['content'], data['content'])

    def test_create_note_invalid(self):
        data = {"medication": 1000000,
                "content": "This note has an invalid medication reference."}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_notes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_details(self):
        note = DoctorsNote.objects.create(
            medication=self.medication,
            content="Initial consultation note."
        )
        url = reverse("doctors_notes-detail", args=[note.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['medication'], self.medication.id)
        self.assertEqual(response.data['content'], note.content)

    def test_delete_note(self):
        note = DoctorsNote.objects.create(
            medication=self.medication,
            content="Note to be deleted."
        )
        url = reverse("doctors_notes-detail", args=[note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DoctorsNote.objects.filter(id=note.id).exists())

    def test_create_missing_fields(self):
        data = {"content": "Missing medication field."}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"medication": self.medication.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_note_not_allowed(self):
        note = DoctorsNote.objects.create(
            medication=self.medication,
            content="Cannot update."
        )
        url = reverse("doctors_notes-detail", args=[note.id])
        response = self.client.put(url, {"content": "Trying update"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
