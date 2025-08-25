from rest_framework.views import APIView
from rest_framework.response import Response
from content_app.models import Video
from .serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated
import os


class VideoListView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
class VideoManifestView(APIView):
    permission_classes = []
    def get(self, request, movie_id, resolution, *args, **kwargs):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        manifest_path = f"media/videos/{video.id}/{resolution}/index.m3u8"
        if not os.path.exists(manifest_path):
            return Response({"error": "Manifest not found"}, status=404)

        with open(manifest_path, 'r') as file:
            manifest_content = file.read()

        return Response(manifest_content, content_type='application/vnd.apple.mpegurl')
    
class VideoSegmentView(APIView):
    permission_classes = []

    def get(self, request, movie_id, resolution, segment, *args, **kwargs):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        segment_path = f"media/videos/{video.id}/{resolution}/{segment}.ts"
        if not os.path.exists(segment_path):
            return Response({"error": "Segment not found"}, status=404)

        with open(segment_path, 'rb') as file:
            segment_content = file.read()

        return Response(segment_content, content_type='video/MP2T')
