from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_admin
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class AuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
