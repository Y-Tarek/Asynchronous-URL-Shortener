from rest_framework import serializers
from .models import ShortenedURL


class ShortenURlSerializer(serializers.ModelSerializer):
    """Serializer for storing urls and shorten them"""
    
    original_url = serializers.URLField()
    class Meta:
         model = ShortenedURL
         fields = ['original_url']
