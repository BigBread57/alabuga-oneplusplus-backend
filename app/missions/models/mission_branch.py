from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class MissionBranch(AbstractBaseModel):
    """
    Ветка миссий.
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
        upload_to="mission_branches",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
    )
    category = models.ForeignKey(
        to="missions.MissionCategory",
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
        related_name="branches",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Ветка миссий")
        verbose_name_plural = _("Ветки миссий")
        ordering = ["category", "order"]

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"
