from rest_framework import serializers


class ShortenURlSerializer(serializers.Serializer):
    """Serializer for storing urls and shorten them"""

    url = serializers.URLField()
