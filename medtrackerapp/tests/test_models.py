from django.test import TestCase
from medtrackerapp.models import Medication, DoseLog
from django.utils import timezone
from datetime import timedelta


class MedicationModelTests(TestCase):

# str method tests
    def test_str_returns_name_and_dosage(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)
        self.assertEqual(str(med), "Aspirin (100mg)")

# tests for adherence_rate method in Medication model
    def test_adherence_rate_all_doses_taken(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)

        now = timezone.now()
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=30))
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=1))

        adherence = med.adherence_rate()
        self.assertEqual(adherence, 100.0)

    def test_adherence_rate_no_log_entries(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)
        adherence = med.adherence_rate()
        self.assertEqual(adherence, 0.0)

    def test_adherence_rate_no_doses_taken(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)

        now = timezone.now()
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=30), was_taken=False)
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=1), was_taken=False)

        adherence = med.adherence_rate()
        self.assertEqual(adherence, 0.0)

    def test_adherence_rate_some_missed_doses(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)

        now = timezone.now()
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=10), was_taken=True)
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=5), was_taken=False)

        adherence = med.adherence_rate()
        self.assertEqual(adherence, 50.0)



# tests for expected_doses method in Medication model
    def test_expected_doses_valid_input(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=3)
        expected = med.expected_doses(10)
        self.assertEqual(expected, 30)

    def test_expected_doses_zero_days(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=3)
        expected = med.expected_doses(0)
        self.assertEqual(expected, 0)

    def test_expected_doses_negative_days_raises_value_error(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=3)
        with self.assertRaises(ValueError):
            med.expected_doses(-5)

    def test_expected_doses_zero_prescribed_per_day_raises_value_error(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=0)
        with self.assertRaises(ValueError):
            med.expected_doses(10)

# tests for adherence_rate_over_period method in Medication model
    def test_adherence_rate_over_period_valid(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=1, prescribed_per_day=1)
        yesterday = timezone.now().date() - timedelta(days=1)
        today = timezone.now().date()
        DoseLog.objects.create(medication=med, taken_at=timezone.now() - timedelta(days=1), was_taken=True)
        self.assertEqual(med.adherence_rate_over_period(yesterday, today), 50.0)

    def test_adherence_rate_over_period_invalid(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=1, prescribed_per_day=1)
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        with self.assertRaises(ValueError):
            med.adherence_rate_over_period(today, yesterday)

    def test_adherence_rate_over_period_expected_doses_zero(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=1, prescribed_per_day=0)
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        with self.assertRaises(ValueError):
            med.adherence_rate_over_period(today, tomorrow)

    def test_adherence_rate_over_period_no_logs(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=1, prescribed_per_day=1)
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        self.assertEqual(med.adherence_rate_over_period(today, tomorrow), 0.0)


class DoseLogModelTests(TestCase):
    def test_doselog_str_taken(self):
        med = Medication.objects.create(name="MedZ", dosage_mg=10, prescribed_per_day=1)
        log = DoseLog.objects.create(
            medication=med,
            taken_at=timezone.now(),
            was_taken=True
        )
        self.assertIn("Taken", str(log))

    def test_doselog_str_missed(self):
        med = Medication.objects.create(name="MedZ", dosage_mg=10, prescribed_per_day=1)
        log = DoseLog.objects.create(
            medication=med,
            taken_at=timezone.now(),
            was_taken=False
        )
        self.assertIn("Missed", str(log))