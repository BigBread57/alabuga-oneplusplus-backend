from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class MissionCompetency(AbstractBaseModel):
    """
    Прокачка компетенций за миссию. Во время выполнения миссии у персонажа могут прокачиваться или
    получаться компетенции.
    """

    mission = models.ForeignKey(
        to="game_world.Mission",
        verbose_name=_("Миссия"),
        help_text=_("Миссия персонажа за успешное выполнение которого он прокачивает компетенцию"),
        on_delete=models.CASCADE,
        related_name="mission_competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        help_text=_("Компетенция, которую прокачивает персонаж по успешному завершению миссии"),
        on_delete=models.CASCADE,
        related_name="mission_competencies",
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Опыт"),
        default=1,
        help_text=_("Сколько получит опыта компетенции за успешное прохождение миссии"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция миссии")
        verbose_name_plural = _("Компетенции миссий")

    def __str__(self):
        return f"{self.mission.name} - {self.competency.name}: +{self.experience}"
