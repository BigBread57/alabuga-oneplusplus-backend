from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class MissionArtifact(AbstractBaseModel):
    """
    Артефакты за выполнение миссии.
    """

    mission = models.ForeignKey(
        Mission,
        verbose_name=_("Миссия"),
        on_delete=models.CASCADE,
    )
    artifact = models.ForeignKey(
        Artifact,
        verbose_name=_("Артефакт"),
        on_delete=models.CASCADE,
    )
    drop_chance = models.FloatField(
        verbose_name=_("Шанс выпадения"),
        default=1.0,
        help_text=_("Вероятность получения артефакта (0.0 - 1.0)"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт миссии")
        verbose_name_plural = _("Артефакты миссий")
        unique_together = ["mission", "artifact"]

    def __str__(self):
        return f"{self.mission.name} - {self.artifact.name}"
