from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class MissionArtifact(AbstractBaseModel):
    """
    Артефакты за выполнение миссии. В редких случаях за выполнение миссии персонажу достается артефакт.
    """

    mission = models.ForeignKey(
        to="game_world.Mission",
        verbose_name=_("Миссия"),
        help_text=_("Миссия персонажа за успешное выполнение которого он сможет получить артефакт"),
        on_delete=models.CASCADE,
        related_name="mission_artifacts",
    )
    artifact = models.ForeignKey(
        to="game_world.Artifact",
        verbose_name=_("Артефакт"),
        help_text=_("Артефакт, который получает персонаж по успешному завершению миссии"),
        on_delete=models.CASCADE,
        related_name="mission_artifacts",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт миссии")
        verbose_name_plural = _("Артефакты миссий")

    def __str__(self):
        return f"{self.mission.name} - {self.artifact.name}"
