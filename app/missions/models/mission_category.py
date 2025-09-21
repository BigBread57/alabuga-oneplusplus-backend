from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class MissionCategory(AbstractBaseModel):
    """
    Категория миссии.
    """

    # QUEST = 'QUEST', _('Квест')
    # RECRUITING = 'RECRUITING', _('Рекрутинг')
    # LECTURING = 'LECTURING', _('Лекторий')
    # SIMULATOR = 'SIMULATOR', _('Симулятор')

    name = models.CharField(
        verbose_name=_("Название категории"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание категории"),
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="competencies",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Категория миссии")
        verbose_name_plural = _("Категории миссий")
        ordering = ("-id",)

    def __str__(self):
        return self.name
