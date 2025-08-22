from django.db import models

# Create your models here.

class Video(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, blank=True)

    original_file = models.FileField(upload_to="videos/", blank=True, null=True)
    hls_directory = models.CharField(max_length=255, blank=True)
    thumbnail_url = models.URLField(blank=True)

    duration_seconds = models.FloatField(null=True, blank=True)
    width_pixels = models.IntegerField(null=True, blank=True)
    height_pixels = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} – {self.title}"
