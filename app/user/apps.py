from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfileConfig(AppConfig):
    """
    Профиль.
    """

    name = 'profile'
    verbose_name = _("Профиль")
