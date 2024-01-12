from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

FIFTEEN_YEARS_IN_DAYS = 15 * 365.25


class User(AbstractUser):
    age = models.DateField(verbose_name='Date de naissance')
    can_be_contacted = models.BooleanField(verbose_name='Peut être contacté', default=False)
    can_data_be_shared = models.BooleanField(verbose_name='Peut partager ses données', default=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    def save(self, *args, **kwargs):
        if self.age:
            fifteen_years_ago = timezone.now() - timezone.timedelta(days=FIFTEEN_YEARS_IN_DAYS)
            is_under_fifteen = self.age >= fifteen_years_ago.date()

            if is_under_fifteen:
                self.can_data_be_shared = not is_under_fifteen

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
