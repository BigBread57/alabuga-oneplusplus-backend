from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


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
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="ranks",
        null=True,
        blank=True,
    )
    required_experience = models.PositiveIntegerField(
        verbose_name=_("Требуемый опыт"),
    )
    order = models.PositiveIntegerField(
        verbose_name=_("Порядок ранга"),
        default=1,
        unique=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Ранг")
        verbose_name_plural = _("Ранги")

    def __str__(self):
        return self.name
