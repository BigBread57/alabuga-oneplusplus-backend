from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class Artifact(AbstractBaseModel):
    """
    Артефакт.
    """

    class Modifiers(models.TextChoices):
        """
        Модификатор.
        """

        DEFAULT = "DEFAULT", _("Стандартный")
        EXPERIENCE_GAIN = "EXPERIENCE_GAIN", _("Прирост опыта")
        MANA_GAIN = "MANA_GAIN", _("Прирост опыта")
        STORE_DISCOUNT = "STORE_DISCOUNT", _("Прирост опыта")

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
        upload_to="competencies",
        null=True,
        blank=True,
    )
    modifier = models.CharField(
        verbose_name=_("Модификатор"),
        max_length=20,
        choices=Modifiers.choices,
        default=Modifiers.DEFAULT,
    )
    modifier_value = models.PositiveIntegerField(
        verbose_name=_("Значение модификатора в %"),
        validators=[MinValueValidator(0)],
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        related_name="artifacts",
    )
    # TODO: ХЗ что это
    # rare = models.CharField(
    #     verbose_name=_("Редкость"),
    #     max_length=20,
    #     blank=True,
    # )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт")
        verbose_name_plural = _("Артефакты")

    def __str__(self):
        return self.name
