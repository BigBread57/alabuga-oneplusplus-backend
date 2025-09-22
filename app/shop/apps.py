from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopConfig(AppConfig):
    """
    Конфиг.
    """

    name = "shop"
    verbose_name = _("Статус помещения")
