from rest_framework import serializers
from content_app.models import Video


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
        fields = ['id', 'created_at', 'title', 'description', 'category']