from uuid import uuid4

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterMissionBranch(AbstractBaseModel):
    """
    Прогресс персонажа по веткам миссиям.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("UUID"),
        default=uuid4,
        unique=True,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Дата и время, когда задача получена"),
        null=True,
        blank=True,
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("Крайняя дата и время задачи, когда она должна быть выполнена"),
        null=True,
        blank=True,
    )
    character = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Персонаж"),
        on_delete=models.CASCADE,
        related_name="character_mission_branches",
    )
    branch = models.ForeignKey(
        to="game_world.MissionBranch",
        verbose_name=_("Ветка"),
        help_text=_("Ветка миссии"),
        on_delete=models.CASCADE,
        related_name="character_mission_branches",
    )
    mentor = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Ментор"),
        on_delete=models.CASCADE,
        related_name="character_mission_branch_mentors",
        null=True,
        blank=True,
        help_text=_("Ментор, который может помочь в выполнении ветки миссий"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Миссия персонажа")
        verbose_name_plural = _("Миссии персонажей")

    def __str__(self):
        return f"{self.character} - {self.branch.name}"

    @cached_property
    def content_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id
