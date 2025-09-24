from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class EventCompetency(AbstractBaseModel):
    """
    Прокачка компетенций за событие.
    """

    event = models.ForeignKey(
        to="game_world.Event",
        verbose_name=_("Миссия"),
        on_delete=models.CASCADE,
        related_name="event_competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        on_delete=models.CASCADE,
        related_name="event_competencies",
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
        return f"{self.event.name} - {self.competency.name}: +{self.experience}"
