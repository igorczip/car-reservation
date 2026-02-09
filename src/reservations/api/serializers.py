from rest_framework import serializers

class ReservationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    note = serializers.CharField(required=False, allow_blank=True)
