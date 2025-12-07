from rest_framework.permissions import BasePermission


class IsAdminOrWriter(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ['admin', 'writer']
        )


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or obj.author == request.user
        )
