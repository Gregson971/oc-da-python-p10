from rest_framework.permissions import BasePermission

from .models import Contributor


def check_contributor(user, project):
    for contributor in Contributor.objects.filter(project_id=project.id):
        if user == contributor.user:
            return True
    return False


class ProjectPermission(BasePermission):
    def has_permission(self, request):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, obj)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author


class IssuePermission(BasePermission):
    def has_permission(self, request):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, obj.project)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author


class CommentPermission(BasePermission):
    pass


class ContributorPermission(BasePermission):
    pass
