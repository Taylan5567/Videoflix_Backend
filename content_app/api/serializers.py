
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
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']


    def get_thumbnail_url(self, obj):
        # Passt den Dateinamen an deine Realität an (jpg/png)
        return f"{settings.MEDIA_URL}videos/{obj.id}/{obj.id}_thumbnail.jpg"