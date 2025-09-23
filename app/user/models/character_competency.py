from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterCompetency(AbstractBaseModel):
    """
    Уровень компетенции персонажа.
    """

    character = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Персонаж"),
        on_delete=models.CASCADE,
        related_name="character_competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        on_delete=models.CASCADE,
        related_name="character_competencies",
    )
    level = models.PositiveIntegerField(
        verbose_name=_("Уровень"),
        default=0,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция персонажа")
        verbose_name_plural = _("Компетенции персонажей")

    def __str__(self):
        return f"{self.character} - {self.competency.name}: {self.level}"
