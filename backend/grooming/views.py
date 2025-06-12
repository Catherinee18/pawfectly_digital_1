from rest_framework import viewsets, permissions
from .models import GroomingAppointment
from .serializers import GroomingAppointmentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class GroomingAppointmentViewSet(viewsets.ModelViewSet):
    queryset = GroomingAppointment.objects.all()
    serializer_class = GroomingAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return GroomingAppointment.objects.select_related("pet__owner")
        return GroomingAppointment.objects.filter(pet__owner=user).select_related("pet__owner")

    
    @action(detail=True, methods=["patch"], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """
        Admin-only endpoint to update the appointment status.
        PATCH /api/grooming/appointments/{id}/update_status/
        Body: { "status": "Confirmed" }
        """
        appointment = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(GroomingAppointment._meta.get_field("status").choices):
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = new_status
        appointment.save()
        return Response({"message": f"Status updated to {new_status}."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="confirmed-slots")
    def confirmed_slots(self, request):
        """
        Custom endpoint: returns confirmed slots for a given date.
        Usage: /api/grooming/appointments/confirmed-slots/?date=YYYY-MM-DD
        """
        date = request.query_params.get("date")
        if not date:
            return Response({"detail": "Date parameter is required."}, status=400)

        appointments = GroomingAppointment.objects.filter(
            appointment_date=date,
            status="Confirmed"
        ).values("appointment_time")

        return Response([appt["appointment_time"].strftime("%H:%M") for appt in appointments])
    # views.py
    
    @action(detail=False, methods=["get"], url_path="confirmed")
    def confirmed_appointments(self, request):
        appointments = GroomingAppointment.objects.filter(status="Confirmed").select_related("pet", "pet__owner")
        data = [
            {
                "title": f"{appt.pet.name} - {appt.service_type}",
                "date": appt.appointment_date.isoformat()
            }
            for appt in appointments
        ]
        return Response(data)
