import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

CONFIRMATION_CODE_LEN = 20


def get_confirmation_code():
    return ''.join(random.choices(
        string.digits + string.ascii_uppercase,
        k=CONFIRMATION_CODE_LEN
    ))


class User(AbstractUser):
    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Confirmation Code'
    )
