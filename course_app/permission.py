from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacherPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, 'teacher'):
            return obj.teacher == request.user

        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user

        if hasattr(obj, 'user'):
            return obj.user == request.user

        return False