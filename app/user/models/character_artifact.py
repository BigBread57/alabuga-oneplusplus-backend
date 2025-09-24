from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class CharacterArtifact(AbstractBaseModel):
    """
    Артефакты персонажа.
    """

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
