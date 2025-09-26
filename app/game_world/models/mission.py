from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Mission(AbstractBaseModel):
    """
    Миссия.
    """

    name = models.CharField(
        verbose_name=_("Название миссии"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание миссии"),
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Награда в опыте"),
        default=0,
    )
    currency = models.PositiveIntegerField(
        verbose_name=_("Награда в валюте"),
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
    order = models.IntegerField(
        verbose_name=_("Порядок в ветке"),
        default=1,
    )
    is_key_mission = models.BooleanField(
        verbose_name=_("Ключевая миссия или нет"),
        default=False,
        help_text=_("Обязательная миссия для получения ранга"),
    )
    is_active = models.BooleanField(
        verbose_name=_("Активная миссия или нет"),
        default=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Время на выполнение в днях"),
        null=True,
        blank=True,
    )
    branch = models.ForeignKey(
        to="game_world.MissionBranch",
        verbose_name=_("Ветка"),
        on_delete=models.CASCADE,
        related_name="missions",
    )
    level = models.ForeignKey(
        to="game_world.MissionLevel",
        on_delete=models.CASCADE,
        verbose_name=_("Уровень"),
        related_name="missions",
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        help_text=_("Игровой мир в рамках которого создается миссия"),
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
        through="game_world.MissionArtifact",
        related_name="missions",
        blank=True,
    )
    competencies = models.ManyToManyField(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенции миссии"),
        through="game_world.MissionCompetency",
        related_name="missions",
        blank=True,
    )
    game_world_stories = GenericRelation(to="game_world.GameWorldStory")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия")
        verbose_name_plural = _("Миссии")

    def __str__(self):
        return self.name
