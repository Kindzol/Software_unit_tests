from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, DoseLogViewSet, DoctorsNoteViewSet

router = DefaultRouter()
router.register("medications", MedicationViewSet, basename="medication")
router.register("logs", DoseLogViewSet, basename="doselog")

router.register("doctors_notes", DoctorsNoteViewSet, basename="doctors_notes")


urlpatterns = [
    path("", include(router.urls)),
]
