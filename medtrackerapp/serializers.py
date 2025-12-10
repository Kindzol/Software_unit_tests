from rest_framework import serializers
from .models import Medication, DoseLog, DoctorsNote


class MedicationSerializer(serializers.ModelSerializer):
    adherence = serializers.SerializerMethodField()

    class Meta:
        model = Medication
        fields = ["id", "name", "dosage_mg", "prescribed_per_day", "adherence"]

    def get_adherence(self, obj):
        return obj.adherence_rate()


class DoseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoseLog
        fields = ["id", "medication", "taken_at", "was_taken"]

class DoctorsNoteSerializer(serializers.ModelSerializer):
    """
    Serializer for DoctorsNote model.

    """
    class Meta:
        model = DoctorsNote
        fields = ["id", "medication", "content", "created_at"]
