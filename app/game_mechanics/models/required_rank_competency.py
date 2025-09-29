from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class RequiredRankCompetency(AbstractBaseModel):
    """
    Требования к компетенциям для получения ранга. Каждый новый ранг имеет определенный набор компетенций, которые
    должны быть получены предыдущим рангом для повышения на новый.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("Используется при генерации объектов через для понимания новый объект или старый"),
        default=uuid4,
        unique=True,
    )
    rank = models.ForeignKey(
        to="game_mechanics.Rank",
        verbose_name=_("Ранг"),
        help_text=_("Ранг, в рамках которого нужно получить определенные компетенции"),
        on_delete=models.CASCADE,
        related_name="required_rank_competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        help_text=_("Компетенция, которую нужно обязательно получить, чтобы повысить ранг"),
        on_delete=models.CASCADE,
        related_name="required_rank_competencies",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Требование к компетенции")
        verbose_name_plural = _("Требования к компетенциям")

    def __str__(self):
        return f"{self.rank} - {self.competency}"
