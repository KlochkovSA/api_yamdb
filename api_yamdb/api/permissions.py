from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class OwnerAndStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        has_auth = request.user.is_authenticated
        is_owner = has_auth and obj.author == request.user
        is_admin = has_auth and request.user.is_admin
        is_moderator = has_auth and request.user.is_moderator

        return is_owner or is_moderator or is_admin