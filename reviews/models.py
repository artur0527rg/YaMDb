from django.db import models
from django.contrib.auth.models import AbstractUser


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE_CHOISES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')
]


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.TextField(
        choices=ROLE_CHOISES,
        default=USER,
        blank=False,
    )

    class Meta:
        ordering = ['username']
