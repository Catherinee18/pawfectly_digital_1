from django.contrib import admin
from .models import PetMatchInteraction

@admin.register(PetMatchInteraction)
class PetMatchInteractionAdmin(admin.ModelAdmin):
    list_display = ('source_pet', 'target_pet', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('source_pet__name', 'target_pet__name')
