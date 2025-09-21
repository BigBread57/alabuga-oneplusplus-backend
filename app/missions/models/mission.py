from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


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
    branch = models.ForeignKey(
        to="mission.MissionBranch",
        verbose_name=_("Ветка"),
        on_delete=models.CASCADE,
        related_name="missions",
    )
    experience = models.IntegerField(
        verbose_name=_("Награда в опыте"),
        default=0,
    )
    mana = models.IntegerField(
        verbose_name=_("Награда в мане"),
        default=0,
    )
    rank = models.ForeignKey(
        to="gamification.Rank",
        verbose_name=_("Ранг миссии"),
        on_delete=models.PROTECT,
        related_name="missions",
        null=True,
        blank=True,
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
        to="gamification.Artifact",
        verbose_name=_("Награды-артефакты"),
        through="MissionArtifact",
        related_name="missions",
        blank=True,
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

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия")
        verbose_name_plural = _("Миссии")
        ordering = ["branch", "order"]

    def __str__(self):
        return self.name
