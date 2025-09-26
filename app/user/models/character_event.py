from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterEvent(AbstractBaseModel):
    """
    Прогресс персонажа по событиям.
    """

    class Statuses(models.TextChoices):
        """
        Статус выполнения миссии.
        """

        IN_PROGRESS = "IN_PROGRESS", _("В процессе")
        COMPLETED = "COMPLETED", _("Выполнена")
        NEED_IMPROVEMENT = "NEED_IMPROVEMENT", _("Требует доработки")
        PENDING_REVIEW = "PENDING_REVIEW", _("На проверке")
        FAILED = "FAILED", _("Провалена")

    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=20,
        choices=Statuses.choices,
        default=Statuses.IN_PROGRESS,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Начата"),
        null=True,
        blank=True,
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("Завершена"),
        null=True,
        blank=True,
    )
    result = models.TextField(
        verbose_name=_("Результат выполнения события"),
        blank=True,
    )
    inspector_comment = models.TextField(
        verbose_name=_("Комментарий проверяющего"),
        blank=True,
    )
    character = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Персонаж"),
        on_delete=models.CASCADE,
        related_name="character_events",
    )
    event = models.ForeignKey(
        to="game_world.Event",
        verbose_name=_("Событие"),
        on_delete=models.CASCADE,
        related_name="character_events",
    )
    inspector = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Проверяющий"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="character_event_inspectors",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Событие персонажа")
        verbose_name_plural = _("События персонажей")

    def __str__(self):
        return f"{self.character} - {self.event.name} ({self.get_status_display()})"
