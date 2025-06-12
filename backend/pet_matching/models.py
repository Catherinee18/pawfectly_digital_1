from django.db import models
from pets.models import Pet

class PetMatchInteraction(models.Model):
    STATUS_CHOICES = [
        ("liked", "Liked"),
        ("matched", "Matched"),
        ("skipped", "Skipped"),
    ]

    source_pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="likes_sent")
    target_pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="likes_received")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source_pet', 'target_pet')

    def __str__(self):
        return f"{self.source_pet.name} → {self.target_pet.name} [{self.status}]"
