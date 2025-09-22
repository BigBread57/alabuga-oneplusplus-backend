from pathlib import Path

from decouple import AutoConfig
from split_settings.tools import include

BASE_DIR = Path(__file__).parent.parent

config = AutoConfig(search_path=BASE_DIR.joinpath("settings"))

include(
    "auth.py",
    "aws.py",
    "celery.py",
    "django.py",
    "debug_tools.py",
    "drf.py",
    "kafka.py",
    "logging.py",
    "sacceptance.py",
    "sentry.py",
)
