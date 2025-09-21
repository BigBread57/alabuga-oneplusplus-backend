from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from app.common.constants import UserRoles

User = get_user_model()


class UserHRPermission(IsAuthenticated):
    """
    Пользователь с ролью HR.
    """

    def has_permission(self, request, view):
        return request.user.role == UserRoles.HR


class UserManagerPermission(IsAuthenticated):
    """
    Пользователь с ролью MANAGER.
    """

    def has_permission(self, request, view):
        return request.user.role == UserRoles.MANAGER


class UserManagerForObjectPermission(UserManagerPermission):
    """
    Пользователь с ролью MANAGER для определенного объекта.
    """


    def has_object_permission(self, request, view, obj):
        """
        Проверка того, что пользователь является менеджером для объекта.
        """
        return obj.manager == request.user
