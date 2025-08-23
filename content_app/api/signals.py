import os
from django.dispatch import receiver
from django.db.models.signals import post_save
from content_app.models import Video
from .tasks import convert_video_to_hls, thumbnail_video
from django_rq import get_queue


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, *args, **kwargs):
    """
    Handles post-save events when a new Video is created.

    Enqueues background tasks to:
    - Convert the uploaded video to HLS format.
    - Generate a thumbnail for the video.

    Args:
        sender (Model): The model class.
        instance (Video): The actual instance being saved.
        created (bool): Whether this is a new instance.
    """
    if not created:
        return

    queue_instance = get_queue("default")
    queue_instance.enqueue(convert_video_to_hls, instance.file.path, instance.id, job_timeout=900)
    queue_instance.enqueue(thumbnail_video, instance.file.path, instance.id, job_timeout=900)
