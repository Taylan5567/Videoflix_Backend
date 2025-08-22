from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=100, blank=True)
    username = models.CharField(email, max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username