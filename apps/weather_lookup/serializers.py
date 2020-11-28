from rest_framework import serializers


class WeatherLookupSerializer(serializers.Serializer):
    """Validate input sent."""
    city = serializers.CharField(max_length=256)
    period = serializers.IntegerField()

    class Meta:
        """Meta class"""
        fields = ['city', 'period']
