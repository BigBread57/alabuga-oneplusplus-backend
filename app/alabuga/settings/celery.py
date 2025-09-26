from django.conf import settings

from alabuga.settings import config

CELERY = {
    "broker_url": config(
        "CELERY_BROKER_URL",
        cast=str,
    ),
    "worker_hijack_root_logger": False,
    "timezone": settings.TIME_ZONE,
}
