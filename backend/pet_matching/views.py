from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PetMatchInteraction
from .serializers import PetMatchInteractionSerializer
from pets.models import Pet

class PetMatchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def suggestions(self, request):
        pet_id = request.query_params.get("pet_id")
        if not pet_id:
            return Response({"error": "Missing pet_id"}, status=400)

        pet = Pet.objects.get(id=pet_id)
        interacted_ids = PetMatchInteraction.objects.filter(source_pet=pet).values_list("target_pet_id", flat=True)

        suggestions = Pet.objects.exclude(id=pet.id).exclude(id__in=interacted_ids)
        data = [{"id": p.id, "name": p.name, "species": p.species, "breed": p.breed, "traits": p.traits} for p in suggestions]
        return Response(data)

    @action(detail=False, methods=["post"])
    def like(self, request):
        source_pet_id = request.data.get("source_pet")
        target_pet_id = request.data.get("target_pet")

        source_pet = Pet.objects.get(id=source_pet_id)
        target_pet = Pet.objects.get(id=target_pet_id)

        # Check if target already liked source → MATCH!
        existing = PetMatchInteraction.objects.filter(
            source_pet=target_pet, target_pet=source_pet, status="liked"
        ).first()

        if existing:
            # Update both to matched
            PetMatchInteraction.objects.update_or_create(
                source_pet=source_pet, target_pet=target_pet,
                defaults={"status": "matched"}
            )
            existing.status = "matched"
            existing.save()
            return Response({"match": True, "message": "It's a match!"})

        # Otherwise, just like
        PetMatchInteraction.objects.update_or_create(
            source_pet=source_pet, target_pet=target_pet,
            defaults={"status": "liked"}
        )
        return Response({"match": False, "message": "Like sent."})

    @action(detail=False, methods=["post"])
    def skip(self, request):
        source_pet_id = request.data.get("source_pet")
        target_pet_id = request.data.get("target_pet")

        PetMatchInteraction.objects.update_or_create(
            source_pet_id=source_pet_id,
            target_pet_id=target_pet_id,
            defaults={"status": "skipped"}
        )
        return Response({"message": "Skipped."})

    @action(detail=False, methods=["get"])
    def matches(self, request):
        pet_id = request.query_params.get("pet_id")
        matches = PetMatchInteraction.objects.filter(source_pet_id=pet_id, status="matched")
        return Response(PetMatchInteractionSerializer(matches, many=True).data)

    @action(detail=False, methods=["get"])
    def matched_user_chat_data(self, request):
        pet_id = request.query_params.get("pet_id")
        if not pet_id:
            return Response({"error": "Missing pet_id"}, status=400)

        matches = PetMatchInteraction.objects.filter(source_pet_id=pet_id, status="matched")
        chat_users = []

        for match in matches:
            matched_pet = match.target_pet
            matched_owner = matched_pet.owner  # assuming Pet model has ForeignKey to CustomUser as `owner`
            chat_users.append({
                "user_id": matched_owner.id,
                "username": matched_owner.username,
                "email": matched_owner.email,
                "matched_pet_name": matched_pet.name,
                "matched_pet_id": matched_pet.id,
            })

        return Response(chat_users)
    @action(detail=False, methods=["get"])
    def liked(self, request):
        pet_id = request.query_params.get("pet_id")
        if not pet_id:
            return Response({"error": "Missing pet_id"}, status=400)

        interactions = PetMatchInteraction.objects.filter(
            source_pet_id=pet_id, status="liked"
        ).select_related("target_pet")

        liked_pets = [
            {
                "id": i.target_pet.id,
                "name": i.target_pet.name,
                "breed": i.target_pet.breed,
                "species": i.target_pet.species,
                "traits": i.target_pet.traits,
            }
            for i in interactions
        ]

        return Response(liked_pets)