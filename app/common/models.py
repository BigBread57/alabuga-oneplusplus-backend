from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    """Базовая модель."""

    created_at = models.DateTimeField(
        verbose_name=_("Дата и время создания объекта"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Дата и время изменения объекта"),
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ("-id",)
