from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class EventArtifact(AbstractBaseModel):
    """
    Артефакты за выполнение миссии.
    """

    event = models.ForeignKey(
        to="game_world.Event",
        verbose_name=_("Событие"),
        on_delete=models.CASCADE,
        related_name="event_artifacts",
    )
    artifact = models.ForeignKey(
        to="game_world.Artifact",
        verbose_name=_("Артефакт"),
        on_delete=models.CASCADE,
        related_name="event_artifacts",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт события")
        verbose_name_plural = _("Артефакты событий")

    def __str__(self):
        return f"{self.event.name} - {self.artifact.name}"
