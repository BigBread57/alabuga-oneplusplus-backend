from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class ActivityCategory(AbstractBaseModel):
    """
    Категория активности. Под активностью понимается событие или миссия. Категории могут представлять собой квесты,
    лектории и др.

    Категории активностей должны быть реальными, чтобы они относились к реальной трудовой деятельности
    на предприятии, но также соотноситься с игровым миром.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("Используется при генерации объектов через для понимания новый объект или старый"),
        default=uuid4,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название категории активности"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Описание категории активности"),
    )
    repeatability = models.PositiveIntegerField(
        verbose_name=_("Через сколько дней повторять активность"),
        help_text=_(
            "Количество дней, через которую данную категории активности стоит повторить. "
            "Используется в некоторых миссиях и событиях. "
            "Например: категория 'Еженедельная миссия', repeatability = 7"
        ),
        null=True,
        blank=True,
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="mission_categories",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Категория активности")
        verbose_name_plural = _("Категории активностей")

    def __str__(self):
        return self.name
