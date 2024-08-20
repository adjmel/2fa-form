from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    enable_2fa = models.BooleanField(default=False)
