from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
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
        COMPLETED = "COMPLETED", _("Завершена")
        NEED_IMPROVEMENT = "NEED_IMPROVEMENT", _("Требует доработки")
        PENDING_REVIEW = "PENDING_REVIEW", _("На проверке")
        FAILED = "FAILED", _("Провалена")

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("UUID"),
        default=uuid4,
        unique=True,
    )
    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=20,
        choices=Statuses.choices,
        default=Statuses.IN_PROGRESS,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Дата и время, когда задача получена"),
        null=True,
        blank=True,
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("Крайняя дата и время задачи, когда она должна быть выполнена"),
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
    final_status_datetime = models.DateTimeField(
        verbose_name=_("Дата и время проставления конечного статуса"),
        null=True,
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
    mentor = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Ментор"),
        on_delete=models.CASCADE,
        related_name="character_event_mentors",
        null=True,
        blank=True,
        help_text=_("Ментор, который может помочь в выполнении миссии"),
    )
    inspector = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Проверяющий"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="character_event_inspectors",
    )
    multimedia = GenericRelation(to="multimedia.Multimedia")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Событие персонажа")
        verbose_name_plural = _("События персонажей")

    def __str__(self):
        return f"{self.character} - {self.event.name} ({self.get_status_display()})"

    @cached_property
    def content_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id
