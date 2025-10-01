from datetime import datetime
from typing import Any

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.services import BaseService
from communication.models import ActivityLog
from game_mechanics.models import Competency, Rank
from game_world.models import MissionArtifact, MissionCompetency
from user.api.v1.services import character_service
from user.models import (
    Character,
    CharacterArtifact,
    CharacterCompetency,
    CharacterEvent,
    CharacterMission,
)
from user.models.character_rank import CharacterRank
from user.tasks import (
    send_mail_about_character_mission_for_character,
    send_mail_about_character_mission_for_inspector,
)


class CharacterMissionService(BaseService):
    """
    Событие персонажа. Сервис.
    """

    @staticmethod
    def _create_or_update_character_artifacts(
        character: Character,
        mission_artifacts: list[MissionArtifact],
    ) -> None:
        """
        При наличии артефактов добавляем их персонажу
        """
        list_character_artifacts = [
            CharacterArtifact(
                character=character,
                artifact=mission_artifact.artifact,
            )
            for mission_artifact in mission_artifacts
        ]
        character_artifacts = CharacterArtifact.objects.bulk_create(
            objs=list_character_artifacts, ignore_conflicts=True
        )

        list_activity_logs = [
            ActivityLog(
                character=character,
                text=_(f"Вы успешно завершили миссию {character_artifact.artifact}. Поздравляем!"),
                content_object=character_artifact,
            )
            for character_artifact in character_artifacts
        ]
        ActivityLog.objects.bulk_create(list_activity_logs)

    @staticmethod
    def _create_or_update_character_competency(
        character: Character,
        mission_competencies: list[MissionCompetency],
        now_datetime: datetime,
    ) -> None:
        """
        Получаем все компетенции, которые относятся к выполняемой миссии.
        Получаем все компетенции пользователя, которые еще не закрыты.
        Добавляем опыт к существующим, создаем новые и закрываем выполненные (при этом создаем следующие)
        """
        character_competencies = {
            character_competency.competency.name: character_competency
            for character_competency in CharacterCompetency.objects.select_related("competency").filter(
                is_received=False
            )
        }
        for mission_competency in mission_competencies:
            competency = mission_competency.competency
            character_competency = character_competencies.get(mission_competency.competency.name)
            new_experience_for_character_competency = character_competency.experience + mission_competency.experience
            # Если опыта за компетенцию получено меньше, чем нужно для ее повышения, то просто сохраняем опыт.
            if new_experience_for_character_competency < competency.required_experience:
                character_competency.experience = new_experience_for_character_competency
                character_competency.save()
            # Если опыта за компетенцию получено больше или равно, чем нужно для ее повышения,
            # то сохраняем максимальный опыт и формируем следующую компетенцию.
            else:
                character_competency.experience = competency.required_experience
                character_competency.received_datetime = now_datetime
                character_competency.is_received = True
                character_competency.save()
                if new_competence := Competency.objects.filter(parent=character_competency.competency).first():
                    new_character_competency, created = CharacterCompetency.objects.update_or_create(
                        character=character,
                        competency=new_competence,
                        defaults={
                            "experience": new_experience_for_character_competency - competency.required_experience,
                        },
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
    def _create_or_update_character_rank(
        character: Character,
        character_mission: CharacterMission,
        now_datetime: datetime,
    ) -> None:
        """
        Создать новый ранг или обновить информацию о старом.
        """
        character_rank = character.character_ranks.filter(is_received=False).first()
        rank = character_rank.rank
        new_experience_for_character_rank = character_rank.experience + character_mission.mission.experience
        Character.objects.filter(
            id=character.id,
        ).update(
            experience=models.F("experience") + character_mission.mission.experience,
            currency=models.F("currency") + character_mission.mission.currency,
        )
        # Если опыта за ранг получено меньше, чем нужно для его повышения, то просто сохраняем опыт.
        if new_experience_for_character_rank < rank.required_experience:
            character_rank.experience = new_experience_for_character_rank
            character_rank.save()
        # Если опыта за ранг получено больше или равно, чем нужно для его повышения,
        # то сохраняем максимальный опыт и формируем следующий ранг.
        else:
            # Сохраняем опыт.
            character_rank.experience = rank.required_experience
            character_rank.save()
            new_rank = Rank.objects.filter(parent=character_rank.rank).first()

            if new_rank and character_service.check_condition_for_new_rank(
                character=character,
                rank=character_rank.rank,
            ):
                character_rank.is_received = True
                character_rank.received_datetime = now_datetime
                # TODO. Есть особенность, что опыт который был получен до соблюдения условий сгорает.
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
                game_world = character.game_world
                character_service.create_new_character_missions(
                    character=character,
                    rank=rank,
                    game_world=game_world,
                    now_datetime=now_datetime,
                )
                character_service.create_character_events(
                    character=character,
                    rank=rank,
                    game_world=game_world,
                    now_datetime=now_datetime,
                )
                character_rank.save()
            else:
                ActivityLog.objects.create(
                    character=character,
                    text=_(f"У вас максимальный ранг {character_rank.rank}. Поздравляем!"),
                    content_object=character_rank.rank,
                )

    def action_post_mission_completed(
        self,
        character: Character,
        character_mission: CharacterMission,
    ):
        """
        Действия после завершения миссии.
        """
        now_datetime = timezone.now()
        ActivityLog.objects.create(
            character=character,
            text=_(f"Вы успешно завершили миссию {character_mission.mission}. Поздравляем!"),
            content_object=character_mission,
        )
        if mission_artifacts := character_mission.mission.mission_artifacts.all():
            self._create_or_update_character_artifacts(
                character=character,
                mission_artifacts=list(mission_artifacts),
            )
        if mission_competencies := character_mission.mission.mission_competencies.select_related("competency").all():
            self._create_or_update_character_competency(
                character=character,
                mission_competencies=list(mission_competencies),
                now_datetime=now_datetime,
            )
        if character_mission.mission.experience > 0:
            self._create_or_update_character_rank(
                character=character,
                character_mission=character_mission,
                now_datetime=now_datetime,
            )

    def update_from_character(
        self,
        character_mission: CharacterMission,
        validated_data: dict[str, Any],
    ) -> CharacterMission:
        """
        Добавление результата к миссии.
        """
        CharacterMission.objects.filter(
            id=character_mission.id,
        ).update(
            status=CharacterMission.Statuses.PENDING_REVIEW,
            **validated_data,
        )
        transaction.on_commit(
            lambda: send_mail_about_character_mission_for_inspector.delay(
                character_mission_id=character_mission.id,
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
        Проверка результата миссии.
        """
        with transaction.atomic():
            CharacterMission.objects.filter(
                id=character_mission.id,
            ).update(
                final_status_datetime=(
                    timezone.now() if validated_data["status"] == CharacterEvent.Statuses.COMPLETED else None
                ),
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
            if character_mission.status == CharacterMission.Statuses.COMPLETED:
                self.action_post_mission_completed(
                    character=character,
                    character_mission=character_mission,
                )
            else:
                ActivityLog.objects.create(
                    character=character,
                    text=_(f"По миссии {character_mission.mission} требуются доработки."),
                    content_object=character_mission,
                )

        transaction.on_commit(
            lambda: send_mail_about_character_mission_for_character.delay(
                character_mission_id=character_mission.id,
            ),
        )
        return character_mission


character_mission_service = CharacterMissionService()
