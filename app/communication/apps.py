from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommunicationConfig(AppConfig):
    """
    Конфиг.
    """

    name = "communication"
    verbose_name = _("Коммуникация")
