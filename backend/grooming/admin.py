from django.contrib import admin
from .models import GroomingAppointment

@admin.register(GroomingAppointment)
class GroomingAppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet', 'service_type', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('service_type', 'status', 'appointment_date')
    search_fields = ('pet__name', 'pet__owner__username')
