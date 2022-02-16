from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Confirmation Code'
    )
