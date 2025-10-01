from datetime import timedelta

from django.utils.timezone import now

from common.constants import QrCodeTypes
from common.services import BaseService
from game_world.models import Event
from user.api.v1.services import character_event_service
from user.models import Character, CharacterEvent


class EventService(BaseService):
    """
    События. Сервис.
    """

    @staticmethod
    def check_qr_code(
        query_params,
        character: Character,
    ) -> None:
        """
        Проверить qr code.
        """
        event_id = query_params.get("event_id")
        type_entity = query_params.get("type_entity")
        qr_code_type = query_params.get("qr_code_type")
        now_datetime = now()

        if type_entity == "event":
            event = Event.objects.get(id=event_id)
            if qr_code_type == QrCodeTypes.CREATE:
                CharacterEvent.objects.get_or_create(
                    character=character,
                    event=event,
                    defaults={
                        "start_datetime": now_datetime,
                        "end_datetime": now_datetime + timedelta(days=event.time_to_complete),
                        "mentor": event.mentor,
                    },
                )
            else:
                character_event = CharacterEvent.objects.get(character=character, event=event)
                character_event.status = CharacterEvent.Statuses.COMPLETED
                character_event.final_status_datetime = now_datetime
                character_event.save()
                character_event_service.action_post_event_completed(
                    character=character,
                    character_event=character_event,
                )


event_service = EventService()
