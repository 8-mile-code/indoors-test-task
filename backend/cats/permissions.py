from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allow access only to object owner."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
