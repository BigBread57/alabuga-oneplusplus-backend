from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class Mission(AbstractBaseModel):
    """
    Миссия.
    """

    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="events",
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name=_("Название миссии"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание миссии"),
    )
    branch = models.ForeignKey(
        to="mission.MissionBranch",
        verbose_name=_("Ветка"),
        on_delete=models.CASCADE,
        related_name="missions",
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Награда в опыте"),
        default=0,
    )
    currency = models.PositiveIntegerField(
        verbose_name=_("Награда в валюте"),
        default=0,
    )
    order = models.IntegerField(
        verbose_name=_("Порядок в ветке"),
        default=1,
    )
    is_key_mission = models.BooleanField(
        verbose_name=_("Ключевая миссия"),
        default=False,
        help_text=_("Обязательная миссия для получения ранга"),
    )
    is_active = models.BooleanField(
        verbose_name=_("Активна"),
        default=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Время на выполнение в днях"),
        null=True,
        blank=True,
    )
    level = models.ForeignKey(
        to="game_world.MissionLevel",
        on_delete=models.CASCADE,
        verbose_name=_("Уровень"),
        related_name="missions",
    )
    required_missions = models.ManyToManyField(
        to="self",
        verbose_name=_("Необходимые миссии"),
        symmetrical=False,
        related_name="unlocks_missions",
        blank=True,
        help_text=_("Миссии, которые нужно выполнить для доступа к этой миссии"),
    )
    artifacts = models.ManyToManyField(
        to="game_world.Artifact",
        verbose_name=_("Награды-артефакты"),
        through="MissionArtifact",
        related_name="missions",
        blank=True,
    )
    competencies = models.ManyToManyField(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенции миссии"),
        through="MissionCompetency",
        related_name="missions",
        blank=True,
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        related_name="missions",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия")
        verbose_name_plural = _("Миссии")

    def __str__(self):
        return self.name
