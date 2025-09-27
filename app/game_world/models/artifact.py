from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Artifact(AbstractBaseModel):
    """
    Артефакт - уникальная награда, которая достается персонажу за прохождение определенных миссий. Только некоторые из
    артефактов имеют модификаторы.
    """

    class Modifiers(models.TextChoices):
        """
        Модификатор.
        """

        DEFAULT = "DEFAULT", _("Стандартный")
        EXPERIENCE_GAIN = "EXPERIENCE_GAIN", _("Прирост опыта")
        CURRENCY_GAIN = "CURRENCY_GAIN", _("Прирост валюты")
        SHOP_DISCOUNT = "SHOP_DISCOUNT", _("Скидка в магазине")

    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название артефакта"),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Описание артефакта"),
        blank=True,
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
        blank=True,
    )
    modifier = models.CharField(
        verbose_name=_("Модификатор"),
        help_text=_(
            "Значение модификатора для артефакта. "
            "Только некоторые артефакты имеют модификатор"
        ),
        max_length=20,
        choices=Modifiers.choices,
        default=Modifiers.DEFAULT,
    )
    modifier_value = models.PositiveIntegerField(
        verbose_name=_("Значение модификатора в %"),
        help_text=_(
            "Значение модификатора в %. На сколько увеличивается тот или иной показатель (обычно не больше 5 %)."
        ),
        validators=[MinValueValidator(0)],
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        help_text=_("Игровой мир в рамках которого создается артефакт"),
        related_name="artifacts",
    )
    game_world_stories = GenericRelation(to="game_world.GameWorldStory")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт")
        verbose_name_plural = _("Артефакты")

    def __str__(self):
        return self.name
