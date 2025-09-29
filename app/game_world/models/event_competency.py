from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class EventCompetency(AbstractBaseModel):
    """
    Прокачка компетенций за событие. Во время выполнения события у персонажа могут прокачиваться или
    получаться компетенции.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("Используется при генерации объектов через для понимания новый объект или старый"),
        default=uuid4,
        unique=True,
    )
    event = models.ForeignKey(
        to="game_world.Event",
        verbose_name=_("Событие"),
        help_text=_("Событие персонажа за успешное выполнение которого он прокачивает компетенцию"),
        on_delete=models.CASCADE,
        related_name="event_competencies",
    )
    competency = models.ForeignKey(
        to="game_mechanics.Competency",
        verbose_name=_("Компетенция"),
        help_text=_("Компетенция, которую прокачивает персонаж по успешному завершению события"),
        on_delete=models.CASCADE,
        related_name="event_competencies",
    )
    experience = models.PositiveIntegerField(
        verbose_name=_("Опыт"),
        default=1,
        help_text=_("Сколько получит опыта компетенции за успешное прохождение события"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Компетенция события")
        verbose_name_plural = _("Компетенции событий")

    def __str__(self):
        return f"{self.event.name} - {self.competency.name}: +{self.experience}"
