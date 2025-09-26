from django.db import models
from django.utils.translation import gettext_lazy as _

from common.constants import CharacterRoles
from common.models import AbstractBaseModel


class Character(AbstractBaseModel):
    """
    Персонаж пользователя.
    """

    avatar = models.ImageField(
        verbose_name=_("Аватар"),
        upload_to="avatars",
        null=True,
        blank=True,
    )
    currency = models.PositiveIntegerField(
        verbose_name=_("Валюта"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активный персонаж или нет"),
        default=True,
    )
    role = models.CharField(
        verbose_name=_("Роль"),
        max_length=20,
        choices=CharacterRoles.choices,
        default=CharacterRoles.CANDIDATE,
    )
    user = models.ForeignKey(
        to="user.User",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="characters",
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        related_name="characters",
    )
    artifacts = models.ManyToManyField(
        to="game_world.Artifact",
        verbose_name=_("Артефакты"),
        through="user.CharacterArtifact",
        related_name="characters",
        blank=True,
    )
    ranks = models.ManyToManyField(
        to="game_mechanics.Rank",
        verbose_name=_("Ранг"),
        through="user.CharacterRank",
        related_name="characters",
        blank=True,
    )
    competencies = models.ManyToManyField(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенции"),
        through="user.CharacterCompetency",
        related_name="characters",
        blank=True,
    )
    missions = models.ManyToManyField(
        to="game_world.Mission",
        verbose_name=_("Миссии"),
        through="user.CharacterMission",
        through_fields=("character", "mission"),
        related_name="characters",
        blank=True,
    )
    events = models.ManyToManyField(
        to="game_world.Event",
        verbose_name=_("События"),
        through="user.CharacterEvent",
        through_fields=("character", "event"),
        related_name="characters",
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Персонаж")
        verbose_name_plural = _("Персонаж")

    def __str__(self):
        return f"{self.user}"
