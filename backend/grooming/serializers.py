from rest_framework import serializers
from .models import GroomingAppointment
from pets.serializers import PetSerializer

class GroomingAppointmentSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)  # ✅ For GET/read views
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=GroomingAppointment._meta.get_field("pet").related_model.objects.all(),
        source="pet",
        write_only=True
    )  # ✅ For POST/write operations

    class Meta:
        model = GroomingAppointment
        fields = '__all__'
        read_only_fields = ['status']
