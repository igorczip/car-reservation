from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

class ReservationViewSet(ViewSet):
    @extend_schema(responses=list)
    def list(self, request):
        return Response([])

    @extend_schema(responses=dict)
    def retrieve(self, request, pk=None):
        return Response({"id": pk})
