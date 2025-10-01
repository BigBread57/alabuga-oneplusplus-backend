from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class MissionBranch(AbstractBaseModel):
    """
    Ветка миссий. Объединяет миссии в одну логическую ветку. Используется для удобной группировки и формированию
    миссий в рамках одной предметной области.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("Используется при генерации объектов через для понимания новый объект или старый"),
        default=uuid4,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название ветки миссий"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_(
            "Описание ветки миссий. "
            "Что должен сделать пользователей в рамках ветки миссий с учетом трудовой деятельности"
        ),
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
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активная ветка миссий или нет"),
        help_text=_("Активная ветка миссий или нет"),
        default=True,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Дата и время для запуска"),
        help_text=_(
            "Дата и время для запуска ветки событий. Используется для создания отложенных веток и "
            "должна сочетать с категорией."
        ),
        null=True,
        blank=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Количество дней на успешное выполнение миссии"),
        help_text=_("Количество дней на успешное выполнение ветки миссиий"),
        null=True,
        blank=True,
    )
    rank = models.ForeignKey(
        to="game_mechanics.Rank",
        verbose_name=_("Ранг ветки миссий"),
        on_delete=models.PROTECT,
        related_name="mission_branches",
        help_text=_("В рамках какого ранга эта ветка событий доступно для выполнения"),
        null=True,
    )
    category = models.ForeignKey(
        to="game_world.ActivityCategory",
        verbose_name=_("Категория"),
        help_text=_("Категория ветки миссии"),
        on_delete=models.CASCADE,
        related_name="mission_branches",
    )
    mentor = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Ментор"),
        on_delete=models.CASCADE,
        related_name="mission_branch_mentors",
        null=True,
        blank=True,
        help_text=_("Ментор, который может помочь в выполнении ветки миссий"),
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        help_text=_("Игровой мир в рамках которого создается ветка миссий"),
        related_name="mission_branches",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Ветка миссий")
        verbose_name_plural = _("Ветки миссий")

    def __str__(self):
        return self.name
