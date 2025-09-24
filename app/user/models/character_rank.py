from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterRank(AbstractBaseModel):
    """
    Ранг персонажа.
    """

    character = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Персонаж"),
        on_delete=models.CASCADE,
        related_name="character_ranks",
    )
    rank = models.ForeignKey(
        to="game_mechanics.Rank",
        on_delete=models.CASCADE,
        verbose_name=_("Ранг"),
        related_name="character_ranks",
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Опыт"),
        default=0,
    )
    is_received = models.BooleanField(
        verbose_name=_("Получен ранг или нет"),
        default=False,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Ранг персонажа")
        verbose_name_plural = _("Ранги персонажей")

    def __str__(self):
        return f"{self.character} - {self.rank.name}: {self.experience}"
