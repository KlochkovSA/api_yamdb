from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    ]

    bio = models.CharField(
        max_length=1000,
        null=True,
        verbose_name="User's biography"
    )
    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Confirmation Code'
    )
    role = models.CharField(
        max_length=50,
        default='user',
        choices=ROLE_CHOICES,
        verbose_name='Role'
    )
    username = models.CharField(max_length=100, unique=True,
                                blank=False, null=False)
    email = models.EmailField(max_length=250, unique=True,
                              blank=False, null=False)

    @property
    def is_admin(self):
        return self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
