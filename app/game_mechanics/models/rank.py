from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Rank(AbstractBaseModel):
    """
    Ранг персонажа. Общий показатель успеха прохождения миссий и событий. Чем больше ты их проходишь, тем выше твой ранг
    и тем больше тебе открывается новых возможностей использования платформы (покупка новых предметов в магазине, более
    интересные миссии). Поле parent указывает на предыдущий ранг (ниже, чем текущий). Ранг имеет только линейный вид:
    Ранг 1 -> Ранг 2 -> Ранг 3 и т.д.
    Ранг имеет только один элемент с parent=None в рамках игрового мира.

    Для получения нового ранга нужно:
    1) Достаточное количество опыта (required_experience), полученного при выполнении заданий.
    2) Выполнение определённых заданий, необходимых для желаемого грейда.
    3) Получение необходимого уровня прокачки конкретных компетенций.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("Используется при генерации объектов через для понимания новый объект или старый"),
        default=uuid4,
        unique=True,
    )
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
            "Количество опыта, которое необходимо получить чтобы полностью " "закрыть ранг и получить новый ранг"
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
