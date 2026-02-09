# src/config/api_urls.py
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from drf_spectacular.utils import extend_schema, inline_serializer


class HealthAPIView(APIView):
    """MVP endpoint pro ověření, že schema generování funguje."""

    @extend_schema(
        responses=inline_serializer(
            name="HealthResponse",
            fields={
                "status": serializers.CharField(),
            },
        )
    )
    def get(self, request):
        return Response({"status": "ok"})


urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="health"),
    path("", include("reservations.api.urls")),
]
