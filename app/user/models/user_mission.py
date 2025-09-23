from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class UserMission(AbstractBaseModel):
    """
    Прогресс пользователя по миссиям.
    """

    class Statuses(models.TextChoices):
        """
        Статус выполнения миссии.
        """

        AVAILABLE = "AVAILABLE", _("Доступна")
        IN_PROGRESS = "IN_PROGRESS", _("В процессе")
        COMPLETED = "COMPLETED", _("Выполнена")
        PENDING_REVIEW = "PENDING_REVIEW", _("На проверке")
        FAILED = "FAILED", _("Провалена")

    user = models.ForeignKey(
        to="user.User",
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="missions",
    )
    mission = models.ForeignKey(
        to="game_mechanics.Mission",
        verbose_name=_("Миссия"),
        on_delete=models.CASCADE,
        related_name="users",
    )
    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=20,
        choices=Statuses.choices,
        default=Statuses.AVAILABLE,
    )
    started_at = models.DateTimeField(
        verbose_name=_("Начата"),
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        verbose_name=_("Завершена"),
        null=True,
        blank=True,
    )
    result = models.TextField(
        verbose_name=_("Результат"),
        blank=True,
        help_text=_("Результат выполнения миссии"),
    )
    inspector = models.ForeignKey(
        to=User,
        verbose_name=_("Проверяющий"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mission_inspectors",
    )
    inspector_comment = models.TextField(
        verbose_name=_("Комментарий проверяющего"),
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия пользователя")
        verbose_name_plural = _("Миссии пользователей")
        unique_together = ["user", "mission"]

    def __str__(self):
        return f"{self.user} - {self.mission.name} ({self.get_status_display()})"
