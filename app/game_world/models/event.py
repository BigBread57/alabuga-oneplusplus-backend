from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Event(AbstractBaseModel):
    """
    Событие.
    """

    name = models.CharField(
        verbose_name=_("Название события"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание события"),
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Награда в опыте"),
        default=0,
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="events",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )
    currency = models.PositiveIntegerField(
        verbose_name=_("Награда в валюте"),
        default=0,
    )
    required_number = models.PositiveIntegerField(
        verbose_name=_("Обязательное количество выполненных миссий для всех игроков"),
        help_text=_("Сколько пользователй должны посетить или закрыть это событие для общего успеха")
    )
    is_active = models.BooleanField(
        verbose_name=_("Активна"),
        default=True,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Дата и время для запуска"),
        null=True,
        blank=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Время на выполнение в днях"),
    )
    category = models.ForeignKey(
        to="game_world.ActivityCategory",
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
        related_name="events",
    )
    rank = models.ForeignKey(
        to="game_mechanics.Rank",
        verbose_name=_("Ранг события"),
        on_delete=models.PROTECT,
        related_name="events",
    )
    artifacts = models.ManyToManyField(
        to="game_world.Artifact",
        verbose_name=_("Артефакты"),
        through="game_world.EventArtifact",
        related_name="events",
        blank=True,
    )
    competencies = models.ManyToManyField(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенции"),
        through="EventCompetency",
        related_name="events",
        blank=True,
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        related_name="events",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия")
        verbose_name_plural = _("Миссии")

    def __str__(self):
        return self.name
