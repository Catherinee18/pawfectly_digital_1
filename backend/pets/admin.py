from django.contrib import admin
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'owner', 'created_at')
    search_fields = ('name', 'species', 'breed', 'owner__username')
    list_filter = ('species', 'age')
