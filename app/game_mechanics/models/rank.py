from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Rank(AbstractBaseModel):
    """
    Ранг пользователя.
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
    required_experience = models.PositiveIntegerField(
        verbose_name=_("Требуемый опыт"),
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="ranks",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        verbose_name=_("Родительский ранг"),
        related_name="children",
        db_index=True,
        null=True,
        blank=True,
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        related_name="ranks",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Ранг")
        verbose_name_plural = _("Ранги")

    def __str__(self):
        return self.name
