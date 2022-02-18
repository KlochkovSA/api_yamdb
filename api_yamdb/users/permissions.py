from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminPermission(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     return (request.user.is_authenticated
    #             or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.ADMIN
