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
