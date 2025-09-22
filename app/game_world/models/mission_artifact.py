from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class MissionArtifact(AbstractBaseModel):
    """
    Артефакты за выполнение миссии.
    """

    mission = models.ForeignKey(
        to="game_world.Mission",
        verbose_name=_("Миссия"),
        on_delete=models.CASCADE,
    )
    artifact = models.ForeignKey(
        to="game_mechanics.Artifact",
        verbose_name=_("Артефакт"),
        on_delete=models.CASCADE,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт миссии")
        verbose_name_plural = _("Артефакты миссий")

    def __str__(self):
        return f"{self.mission.name} - {self.artifact.name}"
