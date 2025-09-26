from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Competency(AbstractBaseModel):
    """
    Компетенция.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название компетенции в рамках игрового мира"),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Описание компетенции в рамках игрового мира"),
        blank=True,
    )
    required_experience = models.PositiveIntegerField(
        verbose_name=_("Требуемый опыт"),
        help_text=_(
            "Количество опыта, которое необходимо получить чтобы полностью "
            "изучить компетенцию и получить новую компетенцию"
        ),
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
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        verbose_name=_("Родительская компетенция"),
        help_text=_(
            "Родительская компетенция. Используется для указания уровней компетенций. "
            "Ссылается на компетенцию уровня ниже"
        ),
        related_name="children",
        db_index=True,
        null=True,
        blank=True,
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        help_text=_("Игровой мир в рамках которого создается компетенция"),
        related_name="competencies",
    )
    game_world_stories = GenericRelation(to="game_world.GameWorldStory")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция")
        verbose_name_plural = _("Компетенции")

    def __str__(self):
        return self.name
