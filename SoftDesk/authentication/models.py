from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    age = models.DateField(verbose_name='Date de naissance')
    can_be_contacted = models.BooleanField(verbose_name='Peut être contacté', default=False)
    can_data_be_shared = models.BooleanField(verbose_name='Peut partager ses données', default=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    def __str__(self):
        return self.username
