import uuid
from django.conf import settings
from django.db import models

ROLES = [('AUTHOR', 'Author'), ('CONTRIBUTOR', 'Contributor')]

TYPES_CHOICES = [('BACKEND', 'Backend'), ('FRONTEND', 'Frontend'), ('IOS', 'iOS'), ('ANDROID', 'Android')]

PRIORITIES_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]

TAGS_CHOICES = [('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')]

STATUSES_CHOICES = [('TODO', 'Todo'), ('IN PROGRESS', 'In progress'), ('DONE', 'Done')]


class Project(models.Model):
    title = models.CharField(max_length=128, verbose_name='Titre')
    description = models.TextField(max_length=2048, verbose_name='Description')
    type = models.CharField(choices=TYPES_CHOICES, max_length=8, verbose_name='Type')
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_author', verbose_name='Auteur'
    )
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, through='Contributor', related_name='contributions', verbose_name='Contributeurs'
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=11, choices=ROLES, default='CONTRIBUTOR')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "project"], name="unique_contributor")]

    def __str__(self):
        return f"{self.user} - {self.role} - {self.project}"


class Issue(models.Model):
    title = models.CharField(max_length=128, verbose_name='Titre')
    description = models.TextField(max_length=2048, verbose_name='Description')
    assigned_to = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name='assigned_issues', null=True, blank=True
    )
    priority = models.CharField(choices=PRIORITIES_CHOICES, max_length=6)
    tag = models.CharField(choices=TAGS_CHOICES, max_length=7)
    status = models.CharField(choices=STATUSES_CHOICES, max_length=11, default='TODO')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField(max_length=2048, verbose_name='Description')
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    def __str__(self):
        return self.description
