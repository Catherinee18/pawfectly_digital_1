from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('pets.urls')),
    path('api/grooming/', include('grooming.urls')),
    path('api/petmatching/', include('pet_matching.urls')),
    path("api/admin/", include("adminpanel.urls")),



]
