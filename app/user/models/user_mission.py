from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class UserMission(AbstractBaseModel):
    """
    Прогресс пользователя по миссиям.
    """

    class Status(models.TextChoices):
        """
        Статус выполнения миссии.
        """

        AVAILABLE = "AVAILABLE", _("Доступна")
        IN_PROGRESS = "IN_PROGRESS", _("В процессе")
        COMPLETED = "COMPLETED", _("Выполнена")
        PENDING_REVIEW = "PENDING_REVIEW", _("На проверке")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="missions",
    )
    mission = models.ForeignKey(
        Mission,
        verbose_name=_("Миссия"),
        on_delete=models.CASCADE,
        related_name="users",
    )
    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
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
        help_text=_("Результат выполнения миссии (ссылки, файлы и т.д.)"),
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Проверил"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_missions",
    )
    review_comment = models.TextField(
        verbose_name=_("Комментарий проверяющего"),
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия пользователя")
        verbose_name_plural = _("Миссии пользователей")
        unique_together = ["user", "mission"]

    def __str__(self):
        return f"{self.user} - {self.mission.name} ({self.get_status_display()})"
