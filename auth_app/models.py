from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    """
    Custom User model with email, username, and password fields.

    Attributes:
        email (EmailField): Optional email address of the user.
        username (CharField): Unique username used for identification.
        password (CharField): Hashed password for the user account.
    """
    email = models.EmailField(max_length=100, blank=True)
    username = models.CharField(email, max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        """
        Return the string representation of the user.

        Returns:
            str: The username of the user instance.
        """
        return self.username