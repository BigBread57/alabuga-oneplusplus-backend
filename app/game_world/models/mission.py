from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Mission(AbstractBaseModel):
    """
    Миссия - это индивидуальное задание пользователя.

    Миссии должны быть реальными, чтобы их можно осуществить при осуществлении трудовой деятельности
    на предприятии, но также соотноситься с игровым миром.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        help_text=_("Название миссии"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание миссии"),
        help_text=_(
            "Описание миссии. "
            "Что должен сделать пользователей в рамках миссии с учетом трудовой деятельности",
    ),
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Награда в опыте"),
        help_text=_("Награда в опыте, которое получит персонаж по завершению миссии"),
        default=0,
    )
    currency = models.PositiveIntegerField(
        verbose_name=_("Награда в валюте"),
        help_text=_("Награда в валюте, которую получит персонаж по завершению миссии"),
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
    order = models.IntegerField(
        verbose_name=_("Порядок в ветке"),
        help_text=_("Порядок в ветке"),
        default=1,
    )
    is_key_mission = models.BooleanField(
        verbose_name=_("Ключевая миссия или нет"),
        help_text=_("Является ли миссия обязательной чтобы получить новый ранг"),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активная миссия или нет"),
        help_text=_("Активная миссия или нет"),
        default=True,
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Количество дней на успешное выполнение миссии"),
        help_text=_("Количество дней на успешное выполнение миссии"),
        null=True,
        blank=True,
    )
    branch = models.ForeignKey(
        to="game_world.MissionBranch",
        verbose_name=_("Ветка"),
        help_text=_("Ветка миссии в рамках которой"),
        on_delete=models.CASCADE,
        related_name="missions",
    )
    level = models.ForeignKey(
        to="game_world.MissionLevel",
        on_delete=models.CASCADE,
        verbose_name=_("Уровень"),
        related_name="missions",
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
        related_name="mission_branches",
        null=True,
        blank=True,
        help_text=_("Ментор, который может помочь в выполнении миссии"),
    )
    game_world = models.ForeignKey(
        to="game_world.GameWorld",
        on_delete=models.CASCADE,
        verbose_name=_("Игровой мир"),
        help_text=_("Игровой мир в рамках которого создается миссия"),
        related_name="missions",
    )
    required_missions = models.ManyToManyField(
        to="self",
        verbose_name=_("Необходимые миссии"),
        symmetrical=False,
        related_name="unlocks_missions",
        blank=True,
        help_text=_("Миссии, которые нужно выполнить для доступа к этой миссии"),
    )
    artifacts = models.ManyToManyField(
        to="game_world.Artifact",
        verbose_name=_("Артефакты"),
        help_text=_("Артефакты, которые может получить персонаж за успешное выполнение миссии"),
        through="game_world.MissionArtifact",
        related_name="missions",
        blank=True,
    )
    competencies = models.ManyToManyField(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенции миссии"),
        help_text=_("Компетенции, которые прокачиваются у персонажа за успешное выполнение миссии"),
        through="game_world.MissionCompetency",
        related_name="missions",
        blank=True,
    )
    game_world_stories = GenericRelation(to="game_world.GameWorldStory")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия")
        verbose_name_plural = _("Миссии")

    def __str__(self):
        return self.name
