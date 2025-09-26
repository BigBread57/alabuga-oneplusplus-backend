from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class MissionLevel(AbstractBaseModel):
    """
    Уровень миссии.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        blank=True,
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="mission_levels",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )
    multiplier_experience = models.PositiveIntegerField(
        verbose_name=_("Множитель опыта от стандартного, в %"),
    )
    multiplier_currency = models.PositiveIntegerField(
        verbose_name=_("Множитель опыта от стандартного, в %"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Уровень миссии")
        verbose_name_plural = _("Уровни миссий")

    def __str__(self):
        return self.name
