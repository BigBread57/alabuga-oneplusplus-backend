from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel

User = get_user_model()


class MissionBranch(AbstractBaseModel):
    """
    Ветка миссий.
    """

    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="mission_branches",
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name=_("Название"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активна"),
        default=True,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Дата и время для запуска"),
        null=True,
        blank=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Время на выполнение в днях"),
        null=True,
        blank=True,
    )
    rank = models.ForeignKey(
        to="game_mechanics.Rank",
        verbose_name=_("Ранг ветки миссий"),
        on_delete=models.PROTECT,
        related_name="mission_branches",
    )
    category = models.ForeignKey(
        to="missions.MissionCategory",
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
        related_name="branches",
    )
    mentor = models.ForeignKey(
        to=User,
        verbose_name=_("Ментор"),
        on_delete=models.CASCADE,
        related_name="mission_categories",
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        related_name="mission_branches",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Ветка миссий")
        verbose_name_plural = _("Ветки миссий")

    def __str__(self):
        return self.name
