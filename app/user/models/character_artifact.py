from uuid import uuid4

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterArtifact(AbstractBaseModel):
    """
    Артефакты персонажа.
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
        related_name="character_artifacts",
    )
    artifact = models.ForeignKey(
        to="game_world.Artifact",
        verbose_name=_("Артефакт"),
        on_delete=models.CASCADE,
        related_name="character_artifacts",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт персонажа")
        verbose_name_plural = _("Артефакты персонажей")

    def __str__(self):
        return f"{self.character} - {self.artifact}"

    @cached_property
    def content_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id
