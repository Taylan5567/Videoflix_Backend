from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from content_app.models import Video
from core import settings
from .serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated
import os


class VideoListView(APIView):
    """
    View to list all videos.
    """
    permission_classes = []
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests and return all videos.

        Parameters
        ----------
        request : Request
            Incoming HTTP request.

        Returns
        -------
        """
        videos = Video.objects.all()
        data = VideoSerializer(videos, many=True).data
        return Response(data) 
    
class VideoManifestView(APIView):
    """
    Serve the HLS playlist (``index.m3u8``) for a given video and resolution.

    Looks for the manifest at:
        ``MEDIA_ROOT/videos/<movie_id>/<resolution>/index.m3u8``

    Returns
    -------
    - 200 with a streamed file response if the manifest exists.
    - 404 JSON if the video or manifest cannot be found.
    """

    permission_classes = []

    def get(self, request, movie_id, resolution, *args, **kwargs):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        manifest_path = os.path.join(
            settings.MEDIA_ROOT, "videos", str(video.id), resolution, "index.m3u8"
        )

        if not os.path.exists(manifest_path):
            return Response({"error": "Manifest not found", "path": manifest_path}, status=404)

        return FileResponse(open(manifest_path, "rb"), content_type="application/vnd.apple.mpegurl")


class VideoSegmentView(APIView):
    """
    Serve a single HLS segment (``*.ts``) for the given video and resolution.

    Looks for the file at:
        ``MEDIA_ROOT/videos/<movie_id>/<resolution>/<segment>``

    Returns
    -------
    - 200 with a streamed file response if the segment exists.
    - 404 JSON if the video or the segment cannot be found.
    """
    permission_classes = []

    def get(self, request, movie_id, resolution, segment, *args, **kwargs):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        segment_path = os.path.join(
            settings.MEDIA_ROOT, "videos", str(video.id), resolution, segment
        )


        if not os.path.exists(segment_path):
            return Response({"error": "Segment not found", "path": segment_path}, status=404)

        return FileResponse(open(segment_path, "rb"), content_type="video/mp2t")
    



class ThumbnailView(APIView):
    """
    Serve the thumbnail image for a given video.
    """

    permission_classes = []

    def get(self, request, movie_id, *args, **kwargs):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

        thumbnail_path = os.path.join(
            settings.MEDIA_ROOT, "videos", str(video.id), f"{video.id}_thumbnail.jpg"
        )

        if not os.path.exists(thumbnail_path):
            return Response({"error": "Thumbnail not found", "path": thumbnail_path}, status=404)

        return FileResponse(open(thumbnail_path, "rb"), content_type="image/jpeg")