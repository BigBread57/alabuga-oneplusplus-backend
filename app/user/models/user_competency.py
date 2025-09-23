from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class UserCompetency(AbstractBaseModel):
    """
    Уровень компетенции пользователя.
    """

    user = models.ForeignKey(
        to="user.User",
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        on_delete=models.CASCADE,
        related_name="user_levels",
    )
    level = models.IntegerField(
        verbose_name=_("Уровень"),
        default=0,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция пользователя")
        verbose_name_plural = _("Компетенции пользователей")
        unique_together = ["user", "competency"]

    def __str__(self):
        return f"{self.user} - {self.competency.name}: {self.level}"
