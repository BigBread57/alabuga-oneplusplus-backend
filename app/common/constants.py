from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    """
    Роли пользователей.
    """

    CANDIDATE = "CANDIDATE", _("Кандидат")
    EMPLOYEE = "EMPLOYEE", _("Сотрудник")
    MANAGER = "MANAGER", _("Менеджер")
    HR = "HR", _("HR")
    ORGANIZER = "ORGANIZER", _("Организатор")
    ADMIN = "ADMIN", _("Администратор")


class Repetitions(models.TextChoices):
    """
    Повторение.
    """

    CONSTANTLY = "CONSTANTLY", _("Постоянно")
    ONCE = "ONCE", _("Один раз")
    ONCE_A_WEEK = "ONCE_A_WEEK", _("Раз в неделю")
    ONCE_A_MONTH = "ONCE_A_MONTH", _("Раз в месяц")
    SPECIFIED_TIME = "SPECIFIED_TIME", _("В указанное время")
