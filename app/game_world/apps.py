from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MissionsConfig(AppConfig):
    """
    Конфиг.
    """

    name = "game_world"
    verbose_name = _("Игровой мир")
