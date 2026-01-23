"""Models for user authentication and profiles.

Contains a `UserProfile` model that can be used to extend or wrap the
built-in Django `User` model. The project primarily uses the auth
system via `django.contrib.auth` and token authentication.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    fullname = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    password_repeated = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.fullname.username
