from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class OwnerAndStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == 'partial_update' or view.action == 'destroy':
            has_auth = request.user.is_authenticated
            return has_auth and (obj.author == request.user
                                 or request.user.is_moderator
                                 or request.user.is_admin)
        return request.method in permissions.SAFE_METHODS
