from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Pet
from .serializers import PetSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    @action(detail=True, methods=["patch"], url_path="upload")
    def upload_image(self, request, pk=None):
        pet = self.get_object()

        if "image" not in request.FILES:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        pet.image = request.FILES["image"]
        pet.save()
        return Response({"image_url": pet.image.url}, status=status.HTTP_200_OK)
