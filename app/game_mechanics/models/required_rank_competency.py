from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class RequiredRankCompetency(AbstractBaseModel):
    """
    Требования к компетенциям для получения ранга.
    """

    rank = models.ForeignKey(
        to="game_mechanics.Rank",
        verbose_name=_("Ранг"),
        on_delete=models.CASCADE,
        related_name="required_competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        on_delete=models.CASCADE,
        related_name="required_ranks",
    )
    required_level = models.PositiveIntegerField(
        verbose_name=_("Требуемый уровень"),
        default=1,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Требование к компетенции")
        verbose_name_plural = _("Требования к компетенциям")

    def __str__(self):
        return f"{self.rank} - {self.competency}: {self.required_level}"
