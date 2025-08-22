from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, blank=True)

    original_file = models.FileField(upload_to="videos/", blank=True, null=True)
    hls_directory = models.CharField(max_length=255, blank=True)
    thumbnail_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
