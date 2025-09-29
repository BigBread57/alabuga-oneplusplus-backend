from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Competency(AbstractBaseModel):
    """
    Компетенция персонажа - это умения и навыки, которы работник может получить в ходе выполнения миссий и событий.
    Например, если есть миссия посетить лекцию по технике безопасности, работник может прокачать компетенцию
    "Безопасная работа". Поле parent указывает на предыдущую компетенцию (ниже, чем текущая). Компетенция имеет только
    линейный вид: Компетенция 1 -> Компетенция 2 -> Компетенция 3 и т.д.
    Компетенция имеет много элементов с parent=None в рамках игрового мира.
    А если есть миссия подготовить доклад по технике безопасности, то прокачать "Ораторское искусство",
    "Ведение диалога", "Безопасная работа".

    Компетенции должны быть реальными, чтобы их можно было получить в ходе осуществления трудовой деятельности
    на предприятии, но также соотноситься с игровым миром.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("Используется при генерации объектов через для понимания новый объект или старый"),
        default=uuid4,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название компетенции в рамках игрового мира"),
        max_length=256,
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
    level = models.PositiveIntegerField(
        verbose_name=_("Уровень компетенции"),
        help_text=_("Уровень компетенции. Повышается на уровень родительской компетенции + 1"),
        default=1,
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
