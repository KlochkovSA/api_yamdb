from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'ad'
    MODERATOR = 'mr'
    USER = 'us'

    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Confirmation Code'
    )

    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=USER
    )

    bio = models.CharField(
        max_length=100,
        null=True,
        verbose_name='User biography'
    )
    email = models.EmailField(blank=False, null=False, unique=True)