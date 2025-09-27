from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterMission(AbstractBaseModel):
    """
    Прогресс персонажа по миссиям.
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
        verbose_name=_("Результат выполнения миссии"),
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
        related_name="character_missions",
    )
    mission = models.ForeignKey(
        to="game_world.Mission",
        verbose_name=_("Миссия"),
        on_delete=models.CASCADE,
        related_name="character_missions",
    )
    inspector = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Проверяющий"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="character_mission_inspectors",
    )
    multimedia = GenericRelation(to="multimedia.Multimedia")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия персонажа")
        verbose_name_plural = _("Миссии персонажей")

    def __str__(self):
        return f"{self.character} - {self.mission.name} ({self.get_status_display()})"

    @cached_property
    def content_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id
