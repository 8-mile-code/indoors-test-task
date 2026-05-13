from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allow access only to object owner."""

    def hase_object_perrmissions(self, request, view, obj):
        return obj.owner == request.user
