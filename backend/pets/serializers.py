from rest_framework import serializers
from .models import Pet
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

class PetSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)  # 👈 This returns full owner details

    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ['owner']
