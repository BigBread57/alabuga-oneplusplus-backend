from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MultimediaConfig(AppConfig):
    """
    Конфиг.
    """

    name = "alabuga_file"
    verbose_name = _("Файлы")
