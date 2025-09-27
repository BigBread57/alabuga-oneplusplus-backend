from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class MissionLevel(AbstractBaseModel):
    """
    Уровень миссии - сложность выполнения той или иной миссии. Сложность должна быть реальной, чтобы миссию
    можно было сделать в рамках трудовой деятельности.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название уровня миссии"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Описание уровня миссии"),
        blank=True,
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="mission_levels",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )
    multiplier_experience = models.PositiveIntegerField(
        verbose_name=_("Множитель опыта от стандартного, в %"),
        help_text=_(
            "Множитель опыта от стандартного, в %. "
            "На сколько процентов увеличивается стандартный размер опыта исходя из сложности миссии"
        ),
    )
    multiplier_currency = models.PositiveIntegerField(
        verbose_name=_("Множитель валюты от стандартного, в %"),
        help_text=_(
            "Множитель валюты от стандартного, в %. "

            "На сколько процентов увеличивается стандартный размер валюты исходя из сложности миссии"
        ),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Уровень миссии")
        verbose_name_plural = _("Уровни миссий")

    def __str__(self):
        return self.name
