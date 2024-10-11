from rest_framework import permissions


class MyIsAuthenticated(permissions.BasePermission):
    message = 'You don\'t have permission to view post lists.'

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAnnaPermission(permissions.BasePermission):
    message = 'You are not allowed to perform this action.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.user == request.user:

            return request.user.username != 'anna' or request.method not in ['PUT', 'PATCH']

        return False
