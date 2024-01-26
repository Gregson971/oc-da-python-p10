from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return request.user == obj
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj
        elif view.action in ['create']:
            return True
