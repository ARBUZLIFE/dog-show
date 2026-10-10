from rest_framework import permissions

from .permissions import user_is_organizer, user_is_chairman, user_is_staff


class IsOrganizerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_is_organizer(request.user)


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_is_staff(request.user)


class IsChairmanOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_is_chairman(request.user)