from common.services import BaseService
from communication.models import ActivityLog
from user.models import Character


class ActivityLogService(BaseService):
    """
    Журнал действий. Сервис.
    """

    @staticmethod
    def read_all(
        character: Character,
    ) -> None:
        """
        Прочитать все записи в журнале событий.
        """
        ActivityLog.objects.filter(character=character).update(is_read=True)
        return None


activity_log_service = ActivityLogService
