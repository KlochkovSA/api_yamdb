from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class OwnerAndStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        has_auth = request.user.is_authenticated
        is_owner = obj.author == request.user
        is_admin = request.user.is_admin
        is_moderator = request.user.is_moderator

        return has_auth and (is_owner or is_moderator or is_admin)
