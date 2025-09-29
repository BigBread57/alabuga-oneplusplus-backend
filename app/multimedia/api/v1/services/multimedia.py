from typing import Any

from common.services import BaseService
from multimedia.models import Multimedia
from user.models import Character


class MultimediaService(BaseService):
    """
    Мультимедиа. Сервис.
    """

    def create(
        self,
        validated_data: dict[str, Any],
        character: Character,
    ) -> Multimedia:
        return Multimedia.objects.create(
            character=character,
            **validated_data,
        )


multimedia_service = MultimediaService()
