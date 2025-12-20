from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WRITER = 'writer', 'Writer'
        READER = 'reader', 'Reader'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.READER
    )

    # Make sure email is unique
    email = models.EmailField(unique=True)

    # ✅ New field to track email verification
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
