from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Topic(AbstractBaseModel):
    """Тема."""

    name = models.CharField(
        verbose_name=_("Название"),
        max_length=256,
    )
    shot_description = models.TextField(
        verbose_name=_("Краткое описание"),
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Тема")
        verbose_name_plural = _("Темы")

    def __str__(self):
        return self.name
