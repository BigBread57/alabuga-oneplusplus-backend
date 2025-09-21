from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    """
    Роли пользователей.
    """

    CANDIDATE = "CANDIDATE", _("Кандидат")
    EMPLOYEE = "EMPLOYEE", _("Сотрудник")
    HR = "HR", _("HR")
    ORGANIZER = "ORGANIZER", _("Организатор")
    ADMIN = "ADMIN", _("Администратор")
