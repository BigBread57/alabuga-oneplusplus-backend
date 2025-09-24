from pathlib import Path

from decouple import AutoConfig
from split_settings.tools import include

BASE_DIR = Path(__file__).parent.parent

config = AutoConfig(search_path=BASE_DIR.joinpath("settings"))

include(
    "django.py",
    "caches.py",
    "celery.py",
    "cors.py",
    "email.py",
    "keycloak.py",
    "llm.py",
    "logging.py",
    "sentry.py",
    "drf.py",
)
