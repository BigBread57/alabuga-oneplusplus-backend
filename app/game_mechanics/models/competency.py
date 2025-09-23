from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Competency(AbstractBaseModel):
    """
    Компетенция.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        blank=True,
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="competencies",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        related_name="competencies",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция")
        verbose_name_plural = _("Компетенции")

    def __str__(self):
        return self.name
