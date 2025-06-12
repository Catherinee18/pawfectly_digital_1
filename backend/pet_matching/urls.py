from django.urls import path
from .views import PetMatchViewSet

match = PetMatchViewSet.as_view({
    "get": "suggestions",
    "post": "like",
})

urlpatterns = [
    path("suggestions/", PetMatchViewSet.as_view({"get": "suggestions"})),
    path("like/", PetMatchViewSet.as_view({"post": "like"})),
    path("skip/", PetMatchViewSet.as_view({"post": "skip"})),
    path("matches/", PetMatchViewSet.as_view({"get": "matches"})),
    path("liked/", PetMatchViewSet.as_view({"get": "liked"})),  # ✅ added
    path("matched_user_chat_data/", PetMatchViewSet.as_view({"get": "matched_user_chat_data"})),  # ✅ added
]