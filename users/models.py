from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"
