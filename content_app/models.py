from django.db import models



class Video(models.Model):

    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'Series'),
        ('documentary', 'Documentary'),
    ]

    title = models.CharField(max_length=200, default="")
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, blank=True, choices=CATEGORY_CHOICES)
    thumbnail_url = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.title
