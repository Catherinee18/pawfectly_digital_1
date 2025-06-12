from rest_framework import serializers
from .models import PetMatchInteraction
from pets.serializers import PetSerializer  # you must create this

class PetMatchInteractionSerializer(serializers.ModelSerializer):
    source_pet = PetSerializer(read_only=True)
    target_pet = PetSerializer(read_only=True)

    class Meta:
        model = PetMatchInteraction
        fields = ['id', 'source_pet', 'target_pet', 'status']
