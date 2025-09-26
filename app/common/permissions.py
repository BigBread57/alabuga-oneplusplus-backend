from rest_framework.permissions import IsAuthenticated

from common.constants import CharacterRoles


class UserHRPermission(IsAuthenticated):
    """
    Пользователь с ролью HR.
    """

    def has_permission(self, request, view):
        return request.user.role == CharacterRoles.HR


class UserManagerPermission(IsAuthenticated):
    """
    Пользователь с ролью MANAGER.
    """

    def has_permission(self, request, view):
        return request.user.role == CharacterRoles.MANAGER


class UserManagerForObjectPermission(UserManagerPermission):
    """
    Пользователь с ролью MANAGER для определенного объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверка того, что пользователь является менеджером для объекта.
        """
        return obj.manager == request.user


class UserInspectorForObjectPermission(UserManagerPermission):
    """
    Пользователь является проверяющим для определенного объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверка того, что пользователь является менеджером для объекта.
        """
        return obj.inspector == request.user or request.user.role == CharacterRoles.HR
