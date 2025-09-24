from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class MissionBranch(AbstractBaseModel):
    """
    Ветка миссий.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        blank=True,
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="mission_branches",
        null=True,
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
        help_text=_("Для какого ранга подходит эта ветка миссий"),
    )
    category = models.ForeignKey(
        to="game_world.ActivityCategory",
        verbose_name=_("Категория миссии"),
        on_delete=models.CASCADE,
        related_name="mission_branches",
    )
    mentor = models.ForeignKey(
        to="user.User",
        verbose_name=_("Ментор"),
        on_delete=models.CASCADE,
        related_name="mission_branches",
        null=True,
        blank=True,
        help_text=_("Ссылка на ментора, который может помочь в выполнении миссии."),
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
