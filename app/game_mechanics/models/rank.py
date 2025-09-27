from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Rank(AbstractBaseModel):
    """
    Ранг персонажа. Общий показатель успеха прохождения миссий и событий. Чем больше ты их проходищь
    """

    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название ранга в рамках игрового мира"),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Описание ранга в рамках игрового мира"),
        blank=True,
    )
    required_experience = models.PositiveIntegerField(
        verbose_name=_("Требуемый опыт"),
        help_text=_(
            "Количество опыта, которое необходимо получить чтобы полностью "
            "закрыть ранг и получить новый ранг"
        ),

    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="ranks",
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
        verbose_name=_("Родительский ранг"),
        help_text=_(
            "Родительский ранг. Используется для указания уровня ранга. "
            "Ссылается на ранг уровня ниже. Ранги имеют линейный вид."
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
        help_text=_("Игровой мир в рамках которого создается ранг"),
        related_name="ranks",
    )
    game_world_stories = GenericRelation(to="game_world.GameWorldStory")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Ранг")
        verbose_name_plural = _("Ранги")

    def __str__(self):
        return self.name
