from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class GameWorldStory(AbstractBaseModel):
    """
    История игрового мира. Маленькие истории об особенностях игрового мира, которые относятся к веткам миссии, миссиям,
    событиям, артефактам, компетенциям и рангам. Истории описывают почему и в каких обстоятельствах было совершено
    действие или создан объект. Истории игрового мира применяются только к некоторым объектам и помогают лучше
    раскрыть игровой мир
    """

    image = models.ImageField(
        verbose_name=_("Изображение"),
        upload_to="history_game_worlds",
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name=_("Текст"),
        help_text=_("Описание истории, лора"),
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        help_text=_("Игровой мир в рамках которого создается история, особенности и описание его предметов и механик"),
        related_name="game_world_stories",
    )
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        verbose_name=_("Тип содержимого"),
        help_text=_("Тип содержимого"),
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Id объекта"),
        help_text=_("Id объекта"),
    )
    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("История игрового мира")
        verbose_name_plural = _("История игрового мира")
