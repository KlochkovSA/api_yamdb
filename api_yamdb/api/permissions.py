from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class ModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'mr'


class RetrieveUpdateDestroyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if (request.method in ['PUT', 'PATCH', 'DELETE']
                and request.user.is_authenticated):
            return (
                obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'mr'
            )
        elif request.method in ['GET']:
            return True
