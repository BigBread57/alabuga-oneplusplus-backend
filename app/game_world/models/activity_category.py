from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class ActivityCategory(AbstractBaseModel):
    """
    Категория активности.
    """

    name = models.CharField(
        verbose_name=_("Название категории"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание категории"),
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
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Категория активности")
        verbose_name_plural = _("Категории активностей")

    def __str__(self):
        return self.name
