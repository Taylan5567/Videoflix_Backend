
import os
from rest_framework import serializers
from content_app.models import Video
from core import settings


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.

    Serializes the following fields:
        - id
        - created_at
        - title
        - description
        - thumbnail_url
        - category
    """
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']


    def get_thumbnail_url(self, obj):
        relative_path = f"thumbnails/{obj.id}_thumbnail.jpg"   
        media_path = settings.BASE_URL + settings.MEDIA_URL + relative_path        
        request = self.context.get("request")
        return request.build_absolute_uri(media_path) if request else media_path