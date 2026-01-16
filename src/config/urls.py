# src/config/urls.py
from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("admin/", admin.site.urls),

    # API v1 (zatím prázdné, ale include musí vracet urlpatterns list)
    path("api/v1/", include("config.api_urls")),

    path("health/", health),
]
