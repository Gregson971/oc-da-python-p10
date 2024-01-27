from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create']:
            return True

        return request.user and request.user.is_authenticated
