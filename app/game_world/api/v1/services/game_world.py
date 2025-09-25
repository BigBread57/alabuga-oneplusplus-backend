from typing import Any

from mypy.checkexpr import defaultdict

from common.services import BaseService
from game_world.models import GameWorld
from user.models import CharacterCompetency
from user.models.character_rank import CharacterRank


class GameWorldService(BaseService):
    """
    Покупки пользователя. Сервис.
    """

    @staticmethod
    def rating(
        game_world: GameWorld,
    ) -> dict[str, Any]:
        """
        Игровой мир. Рейтинг.
        """
        character_ranks = defaultdict(list)
        for character_rank in CharacterRank.objects.select_related(
            "character__user",
            "rank",
        ).filter(
            character__game_world=game_world,
            is_received=False,
        ):
            character_ranks[character_rank.rank.name].append(
                {
                    "user_full_name": character_rank.character.user.full_name(),
                    "rank_name": character_rank.rank.name,
                    "icon": character_rank.rank.icon,
                    "color": character_rank.rank.color,
                    "experience": character_rank.experience,
                }
            )
        character_competencies = defaultdict(list)
        for character_competency in CharacterCompetency.objects.select_related(
            "character__user",
            "competency",
        ).filter(
            character__game_world=game_world,
            is_received=False,
        ):
            character_competencies[character_competency.competency.name].append(
                {
                    "user_full_name": character_competency.character.user.full_name(),
                    "competency_name": character_competency.competency.name,
                    "icon": character_competency.competency.icon,
                    "color": character_competency.competency.color,
                    "experience": character_competency.experience,
                }
            )
        return {
            "character_ranks": character_ranks,
            "character_competencies": character_competencies,
        }

    @staticmethod
    def statistics(
        game_world: GameWorld,
    ) -> dict[str, Any]:
        """
        Игровой мир. Статистика.
        """
        return {
            "character_missions": [],
            "character_events": [],
        }


game_world_service = GameWorldService()
