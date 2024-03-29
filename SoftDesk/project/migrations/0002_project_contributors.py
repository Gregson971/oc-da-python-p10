# Generated by Django 5.0.1 on 2024-01-19 01:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='contributions', through='project.Contributor', to=settings.AUTH_USER_MODEL, verbose_name='Contributeurs'),
        ),
    ]
