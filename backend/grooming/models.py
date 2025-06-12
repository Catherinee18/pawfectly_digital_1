from django.db import models
from pets.models import Pet

class GroomingAppointment(models.Model):
    SERVICE_CHOICES = [
        ("Bath", "Bath"),
        ("Haircut", "Haircut"),
        ("Full Grooming", "Full Grooming"),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="appointments")
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.service_type} on {self.appointment_date} at {self.appointment_time}"
