from rest_framework.viewsets import ViewSet
# ViewSet = sada akcí (list/retrieve/create/update/partial_update/destroy)
# ALE:
# - ViewSet sám o sobě nemá implementované query/DB logiku
# - často se používá pro "ruční" API nebo prototypy

from rest_framework.response import Response
# Response = DRF odpověď, umí vracet JSON podle rendererů (default JSONRenderer)

from drf_spectacular.utils import extend_schema, OpenApiParameter
# extend_schema = ručně doplníš OpenAPI popis (request/response/params/tags/examples...)
# OpenApiParameter = ručně popíšeš parametr (typicky query/path)

from .serializers import ReservationSerializer


class ReservationViewSet(ViewSet):
    # lookup_url_kwarg:
    # - říká DRF routeru/jak se jmenuje proměnná v URL pro detail endpoint
    # - default bývá "pk", ty používáš "id"
    lookup_url_kwarg = "id"

    @extend_schema(responses=ReservationSerializer(many=True))
    # extend_schema(responses=...):
    # - říká drf-spectacular: "odpověď listu je seznam (many=True) ReservationSerializer"
    # - bez toho by spectacular u ViewSetu někdy nevykouzlil správně schema,
    #   protože ViewSet nemá queryset a není to GenericViewSet.

    def list(self, request):
        # list = GET /api/v1/reservations/
        # request = HTTP request objekt (už obsahuje user, auth, query params, atd.)

        return Response([{"id": 1, "note": "Test rezervace"}])
        # Vracíš list dictů => DRF to serializuje do JSON pole.
        # Pozor: tady NEVOLÁŠ serializer, takže:
        # - data nejsou validovaná serializerem
        # - ale pro demo/MVP to nevadí
        # Lepší praxe: ReservationSerializer(data=..., many=True).is_valid(...)
        # nebo rovnou serializer na output: ReservationSerializer(instance=..., many=True).data

    @extend_schema(
        parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)],
        responses=ReservationSerializer,
    )
    # parameters:
    # - ručně říkáš: "v URL je path parametr id typu int"
    # - location=PATH znamená /reservations/{id}/
    #
    # responses=ReservationSerializer:
    # - říkáš: "odpověď je jeden objekt Reservation"

    def retrieve(self, request, id=None):
        # retrieve = GET /api/v1/reservations/{id}/
        # id=None => DRF sem dosadí id z URL

        return Response({"id": int(id), "note": "Detail rezervace"})
        # int(id): pro jistotu převod, ale:
        # - když je router správně, id už typicky bude string z URL
        # - pokud přijde něco nečíselného, tady to spadne ValueError (500)
        # Lepší praxe: validovat id a při chybě vrátit 404/400.
