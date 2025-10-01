from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Event(AbstractBaseModel):
    """
    Событие - это задание, которое распространяется на всех персонажей одновременно и для его выполнения
    необходимо чтобы определенное количество персонажей (required_number) успешно завершили событие.

    События должны быть реальными, чтобы их можно осуществить при осуществлении трудовой деятельности
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
        help_text=_("Название события"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_(
            "Описание события. " "Что должен сделать пользователей в рамках события с учетом трудовой деятельности"
        ),
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Награда в опыте"),
        help_text=_("Награда в опыте, которое получит персонаж по завершению события"),
        default=0,
    )
    currency = models.PositiveIntegerField(
        verbose_name=_("Награда в валюте"),
        help_text=_("Награда в валюте, которую получит персонаж по завершению события"),
        default=0,
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="events",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )
    required_number = models.PositiveIntegerField(
        verbose_name=_("Обязательное количество выполненных событий для всех игроков"),
        help_text=_("Сколько персонажей должны посетить или закрыть это событие для общего успеха"),
    )
    is_active = models.BooleanField(
        verbose_name=_("Активно событие или нет"),
        help_text=_("Активно событие или нет"),
        default=True,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Дата и время для запуска"),
        help_text=_(
            "Дата и время для запуска события. Используется для создания отложенных событий и "
            "должна сочетать с категорией."
        ),
        null=True,
        blank=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Количество дней на успешное выполнение события"),
        help_text=_("Количество дней на успешное выполнение события"),
    )
    qr_code = models.ImageField(
        verbose_name=_("QR код"),
        upload_to="qr_code_events",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        to="game_world.ActivityCategory",
        verbose_name=_("Категория"),
        help_text=_("Категория события"),
        on_delete=models.CASCADE,
        related_name="events",
    )
    rank = models.ForeignKey(
        to="game_mechanics.Rank",
        verbose_name=_("Ранг события"),
        help_text=_("В рамках какого ранга это событие доступно для выполнения"),
        on_delete=models.PROTECT,
        related_name="events",
        null=True,
    )
    artifacts = models.ManyToManyField(
        to="game_world.Artifact",
        verbose_name=_("Артефакты"),
        help_text=_("Артефакты, которые может получить персонаж за успешное выполнение события"),
        through="game_world.EventArtifact",
        related_name="events",
        blank=True,
    )
    competencies = models.ManyToManyField(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенции"),
        help_text=_("Компетенции, которые прокачиваются у персонажа за успешное выполнение события"),
        through="EventCompetency",
        related_name="events",
        blank=True,
    )
    mentor = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Ментор"),
        on_delete=models.CASCADE,
        related_name="events_branches",
        null=True,
        blank=True,
        help_text=_("Ментор, который может помочь в выполнении события"),
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        help_text=_("Игровой мир в рамках которого создается событие"),
        related_name="events",
    )
    game_world_stories = GenericRelation(to="game_world.GameWorldStory")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Событие")
        verbose_name_plural = _("События")

    def __str__(self):
        return self.name
