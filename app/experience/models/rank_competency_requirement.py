from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class RankCompetencyRequirement(AbstractBaseModel):
    """
    Требования к компетенциям для получения ранга.
    """

    rank = models.ForeignKey(
        Rank,
        verbose_name=_("Ранг"),
        on_delete=models.CASCADE,
        related_name="competency_requirements",
    )
    competency = models.ForeignKey(
        Competency,
        verbose_name=_("Компетенция"),
        on_delete=models.CASCADE,
        related_name="rank_requirements",
    )
    level_required = models.IntegerField(
        verbose_name=_("Требуемый уровень"),
        default=1,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Требование к компетенции")
        verbose_name_plural = _("Требования к компетенциям")
        unique_together = ["rank", "competency"]

    def __str__(self):
        return f"{self.rank.name} - {self.competency.name}: {self.level_required}"
