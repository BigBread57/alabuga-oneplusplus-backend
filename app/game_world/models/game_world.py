from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class GameWorld(AbstractBaseModel):
    """
    Игровой мир - мир со своей историей, лором в рамках которого создаются все остальные объекты. Артефакты, ранги,
    описание миссий и все остальные объекты должны иметь общее с игровым миром (часть описания или название должно
    переплетаться с общей идеей мира).
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("Используется при генерации объектов через для понимания новый объект или старый"),
        default=uuid4,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название игрового мира"),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Описание игрового мира"),
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
    )
    standard_experience = models.PositiveIntegerField(
        verbose_name=_("Стандартный размер опыта, начисляемый за очень простую миссию"),
        help_text=_("Стандартный размер опыта, начисляемый за очень простую миссию"),
    )
    standard_currency = models.PositiveIntegerField(
        verbose_name=_("Стандартный размер валюты, начисляемый за очень простую миссию"),
        help_text=_("Стандартный размер валюты, начисляемый за очень простую миссию"),
    )
    currency_name = models.CharField(
        verbose_name=_("Название валюты"),
        help_text=_("Название валюты"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Игровой мир")
        verbose_name_plural = _("Игровые миры")

    def __str__(self):
        return self.name
