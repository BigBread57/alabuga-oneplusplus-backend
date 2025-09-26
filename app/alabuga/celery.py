import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alabuga.settings")

app = Celery("alabuga")
app.config_from_object(settings.CELERY, namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "character-event-failed": {
        "task": "user.tasks.character_event_failed",
        "schedule": crontab(minute="*/1"),
    },
    "character-mission-failed": {
        "task": "user.tasks.character_mission_failed",
        "schedule": crontab(minute="*/1"),
    },
}
