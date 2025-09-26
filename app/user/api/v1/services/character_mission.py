from datetime import timedelta
from typing import Any

from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from common.services import BaseService
from communication.models import ActivityLog
from game_mechanics.models import Competency, Rank, RequiredRankCompetency
from game_world.models import Mission, MissionArtifact, MissionCompetency
from user.models import Character, CharacterArtifact, CharacterCompetency, CharacterMission
from user.models.character_rank import CharacterRank
from user.tasks import send_mail_about_character_mission_for_character, send_mail_about_character_mission_for_inspector


class CharacterMissionService(BaseService):
    """
    Событие персонажа. Сервис.
    """

    @staticmethod
    def create_or_update_character_artifacts(
        character: Character,
        mission_artifacts: list[MissionArtifact],
    ) -> None:
        """
        При наличии артефактов добавляем их персонажу
        """
        character_artifacts = [
            CharacterArtifact(
                character=character,
                artifact=mission_artifact.artifact,
            )
            for mission_artifact in mission_artifacts
        ]
        CharacterArtifact.objects.bulk_create(objs=character_artifacts)

    @staticmethod
    def create_or_update_character_competency(
        character: Character,
        mission_competencies: list[MissionCompetency],
    ) -> None:
        """
        Получаем все компетенции, которые относятся к выполняемой миссии.
        Получаем все компетенции пользователя, которые еще не закрыты.
        Добавляем опыт к существующим, создаем новые и закрываем выполненные (при этом создаем следующие)
        """
        character_competencies = {
            character_competency.competency.id: character_competency
            for character_competency in CharacterCompetency.objects.select_related("competency").filter(
                is_received=False
            )
        }
        for mission_competency in mission_competencies:
            competency = mission_competency.competency
            character_competency = character_competencies.get(mission_competency.competency.id)
            new_experience_for_character_competency = character_competency.experience + mission_competency.experience
            # Если опыта за компетенцию получено меньше, чем нужно для ее повышения, то просто сохраняем опыт.
            if new_experience_for_character_competency < competency.required_experience:
                character_competency.experience = new_experience_for_character_competency
                character_competency.save()
            # Если опыта за компетенцию получено больше или равно, чем нужно для ее повышения,
            # то сохраняем максимальный опыт и формируем следующую компетенцию.
            else:
                character_competency.experience = competency.required_experience
                character_competency.is_received = True
                character_competency.save()
                if new_competence := Competency.objects.filter(parent=character_competency).first():
                    new_character_competency = CharacterCompetency.objects.create(
                        character=character,
                        competency=new_competence,
                        experience=new_experience_for_character_competency - competency.required_experience,
                    )
                    ActivityLog.objects.create(
                        character=character,
                        text=_(
                            f"У вас новая компетенция {new_competence}. Поздравляем!"
                            "Улучшайте свои навыки для получения новых наград"
                        ),
                        content_object=new_character_competency,
                    )
                else:
                    ActivityLog.objects.create(
                        character=character,
                        text=_(f"Вы получили максимальный уровень для {character_competency.competency}. Поздравляем!"),
                        content_object=character_competency,
                    )

    @staticmethod
    def create_or_update_character_rank(
        character: Character,
        character_mission: CharacterMission,
    ) -> None:
        """
        Создать новый ранг или обновить информацию о старом.
        """
        character_rank = character.character_ranks.filter(is_received=False).first()
        rank = character_rank.rank
        new_experience_for_character_rank = character_rank.experience + character_mission.mission.experience
        # Если опыта за ранг получено меньше, чем нужно для его повышения, то просто сохраняем опыт.
        if new_experience_for_character_rank < rank.required_experience:
            character_rank.experience = new_experience_for_character_rank
            character_rank.save()
        # Если опыта за ранг получено больше или равно, чем нужно для его повышения,
        # то сохраняем максимальный опыт и формируем следующий ранг.
        else:
            character_rank.experience = rank.required_experience
            character_rank.is_received = True
            character_rank.save()

            is_required_missions = (
                Mission.objects.filter(rank=character_rank.rank)
                .annotate(
                    required_count=models.Count("required_missions"),
                    completed_required_count=models.Subquery(
                        CharacterMission.objects.filter(
                            character=character,
                            status=CharacterMission.Statuses.COMPLETED,
                            mission__rank=character_rank.rank,
                        )
                        .values("mission")
                        .annotate(count=models.Count("pk", distinct=True))
                        .values("count")[:1]
                    ),
                )
                .filter(required_count=models.F("completed_required_count"))
                .exists()
            )
            is_required_rank_competency = (
                RequiredRankCompetency.objects.filter(
                    rank=character_rank.rank,
                )
                .annotate(
                    required_count=models.Count("pk"),
                    completed_required_count=models.Subquery(
                        CharacterCompetency.objects.filter(
                            character=character,
                            mission__rank=character_rank.rank,
                            is_received=True,
                        )
                        .values("competency")
                        .annotate(count=models.Count("pk", distinct=True))
                        .values("count")[:1]
                    ),
                )
                .filter(required_count=models.F("completed_required_count"))
                .exists()
            )

            new_rank = Rank.objects.filter(parent=character_rank).first()

            if new_rank and is_required_missions and is_required_rank_competency:
                new_character_rank = CharacterRank.objects.create(
                    character=character,
                    rank=new_rank,
                    experience=new_experience_for_character_rank - rank.required_experience,
                )
                ActivityLog.objects.create(
                    character=character,
                    text=_(
                        f"У вас новый ранг {new_character_rank}. Поздравляем!"
                        "Повышайте свой ранг для получения новых наград"
                    ),
                    content_object=new_character_rank,
                )
                now_datetime = now()
                character_missions = [
                    CharacterMission(
                        character=character,
                        mission=mission,
                        start_datetime=now_datetime,
                        end_datetime=now_datetime + timedelta(days=mission.time_to_complete),
                    )
                    for mission in Mission.objects.filter(
                        is_active=True, branch__rank=new_rank, game_world=character.game_world
                    )
                ]
                CharacterMission.objects.bulk_create(objs=character_missions)
            else:
                ActivityLog.objects.create(
                    character=character,
                    text=_(f"У вас максимальный ранг {character_rank.rank}. Поздравляем!"),
                    content_object=character_rank.rank,
                )

    def update_from_character(
        self,
        character_mission: CharacterMission,
        validated_data: dict[str, Any],
    ) -> CharacterMission:
        """
        Создание покупки пользователя.
        """
        CharacterMission.objects.filter(
            id=character_mission.id,
        ).update(
            status=CharacterMission.Statuses.PENDING_REVIEW,
            **validated_data,
        )
        transaction.on_commit(
            lambda: send_mail_about_character_mission_for_inspector.delay(
                character_mission=character_mission.id,
            ),
        )
        character_mission.refresh_from_db()

        return character_mission

    def update_from_inspector(
        self,
        character_mission: CharacterMission,
        validated_data: dict[str, Any],
    ) -> CharacterMission:
        """
        Создание покупки пользователя.
        """
        with transaction.atomic():
            CharacterMission.objects.filter(
                id=character_mission.id,
            ).update(
                **validated_data,
            )
            character_mission = (
                CharacterMission.objects.select_related(
                    "inspector",
                    "character__user",
                    "mission",
                    "character",
                )
                .prefetch_related(
                    "mission__artifacts",
                    "mission__mission_artifacts",
                    "mission__competencies",
                    "mission__mission_competencies",
                )
                .get(id=character_mission.id)
            )
            character = character_mission.character
            if mission_artifacts := character_mission.mission.mission_artifacts.all():
                self.create_or_update_character_artifacts(
                    character=character,
                    mission_artifacts=list(mission_artifacts),
                )
            if character_mission.status == CharacterMission.Statuses.COMPLETED:
                if mission_competencies := character_mission.mission.mission_competencies.select_related(
                    "competency"
                ).all():
                    self.create_or_update_character_competency(
                        character=character,
                        mission_competencies=list(mission_competencies),
                    )
                if character_mission.mission.experience > 0:
                    self.create_or_update_character_rank(
                        character=character,
                        character_mission=character_mission,
                    )
                character.currency = character.currency + character_mission.mission.currency
                character.save()
                ActivityLog.objects.create(
                    character=character,
                    text=_(f"Вы успешно завершили миссию {character_mission.mission}. Поздравляем!"),
                    content_object=character_mission,
                )
            else:
                ActivityLog.objects.create(
                    character=character,
                    text=_(f"По миссии {character_mission.mission} требуются доработки."),
                    content_object=character_mission,
                )

        transaction.on_commit(
            lambda: send_mail_about_character_mission_for_character.delay(
                character_mission=character_mission.id,
            ),
        )
        return character_mission


character_mission_service = CharacterMissionService()
