from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.constants import CharacterRoles
from user.models import CharacterEvent, CharacterMission, User


@shared_task
def send_mail_about_character_event_for_inspector(
    character_event_id: int,
) -> None:
    """
    Отправить уведомление на почту проверяющему или hr.
    """
    character_event = CharacterEvent.objects.select_related(
        "inspector",
        "character__user",
        "event",
        "character",
    ).get(id=character_event_id)
    inspector_emails = (
        [character_event.inspector.email]
        if character_event.inspector
        else list(User.objects.filter(role=CharacterRoles.HR).values_list("email", flat=True))
    )
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    send_mail(
        subject=_(f"Пользователь №{character_event.character.user.full_name} завершил событие"),
        message=(
            f"Событие: {character_event.event.name}\n"
            f"Результат пользователя: {character_event.result}\n"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=inspector_emails,
    )
    return None


@shared_task
def send_mail_about_character_event_for_character(
    character_event_id: int,
) -> None:
    """
    Отправить уведомление на почту пользователю.
    """
    character_event = CharacterEvent.objects.select_related(
        "inspector",
        "character__user",
        "event",
        "character",
    ).get(id=character_event_id)
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    send_mail(
        subject=_(f"Новый статус по {character_event.event.name}"),
        message=(
            f"Событие: {character_event.event.name}\n"
            f"Комментарий проверяющего: {character_event.inspector_comment}\n"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[character_event.character.user.email],
    )
    return None


@shared_task
def send_mail_about_character_mission_for_inspector(
    character_mission_id: int,
) -> None:
    """
    Отправить уведомление на почту проверяющему или hr.
    """
    character_mission = CharacterMission.objects.select_related(
        "inspector",
        "character__user",
        "mission",
        "character",
    ).get(id=character_mission_id)
    inspector_emails = (
        [character_mission.inspector.email]
        if character_mission.inspector
        else list(User.objects.filter(role=CharacterRoles.HR).values_list("email", flat=True))
    )
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    send_mail(
        subject=_(f"Пользователь №{character_mission.character.user.full_name} завершил миссию"),
        message=(
            f"Миссия: {character_mission.mission.name}\n"
            f"Результат пользователя: {character_mission.result}\n"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=inspector_emails,
    )
    return None


@shared_task
def send_mail_about_character_mission_for_character(
    character_mission_id: int,
) -> None:
    """
    Отправить уведомление на почту пользователю.
    """
    character_mission = CharacterMission.objects.select_related(
        "inspector",
        "character__user",
        "mission",
        "character",
    ).get(id=character_mission_id)
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    send_mail(
        subject=_(f"Новый статус по {character_mission.mission.name}"),
        message=(
            f"Миссия: {character_mission.mission.name}\n"
            f"Комментарий проверяющего: {character_mission.inspector_comment}\n"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[character_mission.character.user.email],
    )
    return None


@shared_task
def character_event_failed() -> None:
    """
    События персонажа провалены.
    """
    CharacterEvent.objects.filter(
        status=CharacterEvent.Statuses.IN_PROGRESS,
        end_datetime__lte=timezone.now(),
    ).update(status=CharacterEvent.Statuses.FAILED)


@shared_task
def character_mission_failed() -> None:
    """
    Миссии персонажа провалены.
    """
    CharacterMission.objects.filter(
        status=CharacterMission.Statuses.IN_PROGRESS,
        end_datetime__lte=timezone.now(),
    ).update(status=CharacterMission.Statuses.FAILED)
