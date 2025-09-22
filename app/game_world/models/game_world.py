from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class GameWorld(AbstractBaseModel):
    """
    Игровой мир.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
    )
    standard_experience = models.PositiveIntegerField(
        verbose_name=_("Стандартный размер опыта, начисляемый за очень простую миссию"),
    )
    standard_currency = models.PositiveIntegerField(
        verbose_name=_("Стандартный размер валюты, начисляемый за очень простую миссию"),
    )
    currency_name = models.CharField(
        verbose_name=_("Название валюты"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Игровой мир")
        verbose_name_plural = _("Игровые миры")

    def __str__(self):
        return self.name
