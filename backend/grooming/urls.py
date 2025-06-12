from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroomingAppointmentViewSet

router = DefaultRouter()
router.register(r'appointments', GroomingAppointmentViewSet, basename='grooming-appointment')

urlpatterns = [
    path('', include(router.urls)),
]
