from typing import Any

from django.db import models

from common.services import BaseService
from game_mechanics.models import Competency
from game_world.models import Artifact, Event, Mission, MissionLevel
from user.models import Character, CharacterCompetency, CharacterEvent, CharacterMission


class CharacterService(BaseService):
    """
    Персонаж пользователя. Сервис.
    """

    def statistics(
        self,
        character: Character,
    ) -> dict[str, Any]:
        """
        Персонаж пользователя. Статистика.
        """
        mission_level_names = MissionLevel.objects.values_list("name", flat=True).distinct()
        filters = {
            mission_level_name: models.Count(
                "id",
                filter=models.Q(mission__level__name=mission_level_name),
                distinct=True,
            )
            for mission_level_name in mission_level_names
        }
        character_mission_level_statistics = character.character_missions.filter(mission__isnull=False).aggregate(
            **filters
        )

        game_world_statistics = {
            "total_missions": Mission.objects.filter(game_world=character.game_world, is_active=True).count(),
            "total_events": Event.objects.filter(game_world=character.game_world, is_active=True).count(),
            "total_artifacts": Artifact.objects.filter(game_world=character.game_world).count(),
            "total_competencies": Competency.objects.filter(game_world=character.game_world).count(),
        }
        character_competencies = [
            {
                "item": character_competency.competency.name,
                "type": "Твой уровень компетенции",
                "score": character_competency.competency.level,
            }
            for character_competency in CharacterCompetency.objects.select_related("competency")
            .filter(
                character=character,
                is_received=False,
            )
            .order_by("competency__name")
        ]
        avg_character_competencies = [
            {
                "item": character_competency.competency.name,
                "type": "Средний уровень компетенции",
                "score": character_competency.avg_level,
            }
            for character_competency in CharacterCompetency.objects.select_related("competency")
            .filter(
                is_received=False,
            )
            .annotate(avg_level=models.Avg("competency__level"))
            .order_by("competency__name")
        ]

        return {
            "missions": {
                "total_missions": game_world_statistics["total_missions"],
                "total_character_missions": character.total_missions,
                "by_status": [
                    {
                        "type": CharacterMission.Statuses.COMPLETED.label,
                        "value": character.completed_missions,
                    },
                    {
                        "type": CharacterMission.Statuses.IN_PROGRESS.label,
                        "value": character.in_progress_missions,
                    },
                    {
                        "type": CharacterMission.Statuses.NEED_IMPROVEMENT.label,
                        "value": character.need_improvement_missions,
                    },
                    {
                        "type": CharacterMission.Statuses.PENDING_REVIEW.label,
                        "value": character.pending_review_missions,
                    },
                    {
                        "type": CharacterMission.Statuses.FAILED.label,
                        "value": character.failed_missions,
                    },
                ],
                "by_level": [
                    {"type": key, "value": value} for key, value in character_mission_level_statistics.items()
                ],
                "completion_rate": (
                    character.completed_missions / character.total_missions * 100 if character.total_missions > 0 else 0
                ),
            },
            "events": {
                "total_events": game_world_statistics["total_events"],
                "total_character_events": character.total_events,
                "by_status": [
                    {
                        "type": CharacterEvent.Statuses.COMPLETED.label,
                        "value": character.completed_events,
                    },
                    {
                        "type": CharacterEvent.Statuses.IN_PROGRESS.label,
                        "value": character.in_progress_events,
                    },
                    {
                        "type": CharacterEvent.Statuses.NEED_IMPROVEMENT.label,
                        "value": character.need_improvement_events,
                    },
                    {
                        "type": CharacterEvent.Statuses.PENDING_REVIEW.label,
                        "value": character.pending_review_events,
                    },
                    {
                        "type": CharacterEvent.Statuses.FAILED.label,
                        "value": character.failed_events,
                    },
                ],
                "completion_rate": (
                    character.completed_events / character.total_events * 100 if character.total_events > 0 else 0
                ),
            },
            "artifacts": {
                "total_artifacts": game_world_statistics["total_artifacts"],
                "total_character_artifacts": character.total_artifacts,
                "by_type": [
                    {
                        "type": Artifact.Modifiers.DEFAULT.label,
                        "value": character.default_artifacts,
                    },
                    {
                        "type": Artifact.Modifiers.EXPERIENCE_GAIN.label,
                        "value": character.experience_gain_artifacts,
                    },
                    {
                        "type": Artifact.Modifiers.CURRENCY_GAIN.label,
                        "value": character.currency_gain_artifacts,
                    },
                    {
                        "type": Artifact.Modifiers.SHOP_DISCOUNT.label,
                        "value": character.shop_discount_artifacts,
                    },
                ],
            },
            "competencies": {
                "total_competencies": game_world_statistics["total_competencies"],
                "total_character_competencies": character.total_competencies,
                "by_name": [
                    *character_competencies,
                    *avg_character_competencies,
                ],
            },
        }


character_service = CharacterService()
