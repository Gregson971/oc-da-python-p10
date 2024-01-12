from django.contrib import admin
from .models import Project, Issue, Comment, Contributor


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'type', 'author', 'created_time')


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'assigned_to',
        'priority',
        'tag',
        'status',
        'project',
        'author',
        'created_time',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'uuid', 'author', 'issue', 'created_time')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'role', 'created_time')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)
