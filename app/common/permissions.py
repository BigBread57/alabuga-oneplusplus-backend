from rest_framework.permissions import IsAuthenticated

from common.constants import CharacterRoles


class CharacterHrPermission(IsAuthenticated):
    """
    Пользователь с ролью HR.
    """

    def has_permission(self, request, view):
        return request.user.active_character.role == CharacterRoles.HR


class CharacterContentManagerPermission(IsAuthenticated):
    """
    Пользователь с ролью CONTENT_MANAGER.
    """

    def has_permission(self, request, view):
        return request.user.active_character.role == CharacterRoles.CONTENT_MANAGER


class UserManagerPermission(IsAuthenticated):
    """
    Пользователь с ролью MANAGER.
    """

    def has_permission(self, request, view):
        return request.user.active_character.role == CharacterRoles.MANAGER


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
        return obj.inspector == request.user or request.user.active_character.role == CharacterRoles.HR
