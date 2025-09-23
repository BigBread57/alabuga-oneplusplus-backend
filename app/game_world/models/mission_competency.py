from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class MissionCompetency(AbstractBaseModel):
    """
    Прокачка компетенций за миссию.
    """

    mission = models.ForeignKey(
        to="game_world.Mission",
        verbose_name=_("Миссия"),
        on_delete=models.CASCADE,
        related_name="competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        on_delete=models.CASCADE,
        related_name="missions",
    )
    experience = models.IntegerField(
        verbose_name=_("Очки прокачки"),
        default=1,
        help_text=_("На сколько повысится уровень компетенции"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция миссии")
        verbose_name_plural = _("Компетенции миссий")

    def __str__(self):
        return f"{self.mission.name} - {self.competency.name}: +{self.experience}"
