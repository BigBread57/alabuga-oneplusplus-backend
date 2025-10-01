from uuid import uuid4

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterCompetency(AbstractBaseModel):
    """
    Уровень компетенции персонажа.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("UUID"),
        default=uuid4,
        unique=True,
    )
    character = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Персонаж"),
        on_delete=models.CASCADE,
        related_name="character_competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        on_delete=models.CASCADE,
        related_name="character_competencies",
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Опыт"),
        default=0,
    )
    is_received = models.BooleanField(
        verbose_name=_("Получена компетенция или нет"),
        default=False,
    )
    received_datetime = models.DateTimeField(
        verbose_name=_("Дата и время получения"),
        null=True,
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция персонажа")
        verbose_name_plural = _("Компетенции персонажей")

    def __str__(self):
        return f"{self.character} - {self.competency.name}: {self.experience}"

    @cached_property
    def content_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id
