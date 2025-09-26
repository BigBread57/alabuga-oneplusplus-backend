from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Topic(AbstractBaseModel):
    """
    Тема.
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
        upload_to="topics",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )
    game_worlds = models.ManyToManyField(
        to="game_world.GameWorld",
        verbose_name=_("Игровой мир"),
        related_name="topics",
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Тема")
        verbose_name_plural = _("Темы")

    def __str__(self):
        return self.name
