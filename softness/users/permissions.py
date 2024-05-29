from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, _, obj) -> bool:
        return obj.user == request.user
