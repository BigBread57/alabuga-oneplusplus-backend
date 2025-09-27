from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class EventArtifact(AbstractBaseModel):
    """
    Артефакты за выполнение события. В редких случаях за выполнение события персонажу достается артефакт.
    """

    event = models.ForeignKey(
        to="game_world.Event",
        verbose_name=_("Событие"),
        help_text=_("Событие персонажа за успешное выполнение которого он сможет получить артефакт"),
        on_delete=models.CASCADE,
        related_name="event_artifacts",
    )
    artifact = models.ForeignKey(
        to="game_world.Artifact",
        verbose_name=_("Артефакт"),
        help_text=_("Артефакт, который получает персонаж по успешному завершению события"),
        on_delete=models.CASCADE,
        related_name="event_artifacts",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт события")
        verbose_name_plural = _("Артефакты событий")

    def __str__(self):
        return f"{self.event.name} - {self.artifact.name}"
