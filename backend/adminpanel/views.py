from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from grooming.models import GroomingAppointment
from pet_matching.models import PetMatchInteraction
from pets.models import Pet
from collections import defaultdict
from datetime import datetime

User = get_user_model()

class AdminViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response({
            "users": User.objects.count(),
            "pets": Pet.objects.count(),
            "matches": PetMatchInteraction.objects.filter(status="matched").count(),
            "appointments": GroomingAppointment.objects.count(),
        })

    @action(detail=False, methods=['get'])
    def list_users(self, request):
        users = User.objects.all().values('id', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'date_joined')
        return Response(list(users))

    @action(detail=False, methods=['get'])
    def appointments_by_date(self, request):
        appointments = GroomingAppointment.objects.all().order_by('appointment_date')
        grouped = defaultdict(list)

        for appt in appointments:
            date_str = appt.appointment_date.strftime("%Y-%m-%d")
            grouped[date_str].append({
                "id": appt.id,
                "pet": appt.pet.name,
                "service": appt.service_type,
                "time": appt.appointment_time.strftime("%H:%M"),
                "status": appt.status,
            })

        return Response(grouped)
