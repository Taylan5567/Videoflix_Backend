from django.db import models

class Video(models.Model):
    """
    Model representing a video resource.
    """

    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'Series'),
        ('documentary', 'Documentary'),
        ('romance', 'Romance'),
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('horror', 'Horror'),
        ('thriller', 'Thriller'),
        ('sci-fi', 'Sci-Fi'),
        ('fantasy', 'Fantasy'),
    ]

    title = models.CharField(max_length=200, default="")
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, blank=True, choices=CATEGORY_CHOICES)
    thumbnail_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='videos/', blank=True, null=True)


    @property
    def thumbnail_url(self):
        if not self.file:
            return None
        return f"/media/thumbnails/{self.id}_thumbnail.jpg"

    def __str__(self):
        return self.title
