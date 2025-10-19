from datetime import datetime
from typing import Any

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.services import BaseService
from communication.models import ActivityLog
from game_mechanics.models import Competency, Rank
from game_world.models import EventArtifact, EventCompetency
from user.api.v1.services import character_service
from user.models import (
    Character,
    CharacterArtifact,
    CharacterCompetency,
    CharacterEvent,
)
from user.models.character_rank import CharacterRank
from user.tasks import (
    send_mail_about_character_event_for_character,
    send_mail_about_character_event_for_inspector,
)


class CharacterEventService(BaseService):
    """
    Событие персонажа. Сервис.
    """

    @staticmethod
    def _create_or_update_character_artifacts(
        character: Character,
        event_artifacts: list[EventArtifact],
    ) -> None:
        """
        При наличии артефактов добавляем их персонажу
        """
        list_activity_logs = []
        for event_artifact in event_artifacts:
            character_artifact, created = CharacterArtifact.objects.get_or_create(
                character=character,
                artifact=event_artifact.artifact,
            )
            list_activity_logs.append(
                ActivityLog(
                    character=character,
                    text=_(f"Вы успешно завершили событие {character_artifact.artifact}. Поздравляем!"),
                    content_object=character_artifact,
                )
            )
        ActivityLog.objects.bulk_create(list_activity_logs)

    @staticmethod
    def _create_or_update_character_competency(
        character: Character,
        event_competencies: list[EventCompetency],
        now_datetime: datetime,
    ) -> None:
        """
        Получаем все компетенции, которые относятся к выполняемому события.
        Получаем все компетенции пользователя, которые еще не закрыты.
        Добавляем опыт к существующим, создаем новые и закрываем выполненные (при этом создаем следующие)
        """
        character_competencies = {
            character_competency.competency.name: character_competency
            for character_competency in CharacterCompetency.objects.select_related("competency").filter(
                is_received=False,
            )
        }
        for event_competency in event_competencies:
            competency = event_competency.competency
            character_competency = character_competencies.get(event_competency.competency.name)
            new_experience_for_character_competency = character_competency.experience + event_competency.experience
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
        character_event: CharacterEvent,
        now_datetime: datetime,
    ) -> None:
        """
        Создать новый ранг или обновить информацию о старом.
        """
        character_rank = character.character_ranks.filter(is_received=False).first()
        rank = character_rank.rank
        new_rank = Rank.objects.filter(parent=character_rank.rank).first()
        new_experience_for_character_rank = character_rank.experience + character_event.event.experience
        Character.objects.filter(
            id=character.id,
        ).update(
            experience=models.F("experience") + character_event.event.experience,
            currency=models.F("currency") + character_event.event.currency,
        )
        if not new_rank:
            return None
        # Если опыта за ранг получено меньше, чем нужно для его повышения, то просто сохраняем опыт.
        if new_experience_for_character_rank < new_rank.required_experience:
            character_rank.experience = new_experience_for_character_rank
            character_rank.save()
        # Если опыта за ранг получено больше или равно, чем нужно для его повышения,
        # то сохраняем максимальный опыт и формируем следующий ранг.
        else:
            # Сохраняем опыт.
            character_rank.experience = new_rank.required_experience
            character_rank.save()
            if new_rank and character_service.check_condition_for_new_rank(
                character=character, rank=character_rank.rank
            ):
                character_rank.is_received = True
                character_rank.received_datetime = now_datetime
                character_rank.save()
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
            else:
                ActivityLog.objects.create(
                    character=character,
                    text=_(f"У вас максимальный ранг {character_rank.rank}. Поздравляем!"),
                    content_object=character_rank.rank,
                )

    def action_post_event_completed(
        self,
        character: Character,
        character_event: CharacterEvent,
    ):
        """
        Действия после завершения события.
        """
        now_datetime = timezone.now()
        ActivityLog.objects.create(
            character=character,
            text=_(f"Вы успешно завершили событие {character_event.event}. Поздравляем!"),
            content_object=character_event,
        )
        if event_artifacts := character_event.event.event_artifacts.all():
            self._create_or_update_character_artifacts(
                character=character,
                event_artifacts=list(event_artifacts),
            )
        if event_competencies := character_event.event.event_competencies.select_related("competency").all():
            self._create_or_update_character_competency(
                character=character,
                event_competencies=list(event_competencies),
                now_datetime=now_datetime,
            )
        if character_event.event.experience > 0:
            self._create_or_update_character_rank(
                character=character,
                character_event=character_event,
                now_datetime=now_datetime,
            )

    def update_from_character(
        self,
        character_event: CharacterEvent,
        validated_data: dict[str, Any],
    ) -> CharacterEvent:
        """
        Создание покупки пользователя.
        """
        CharacterEvent.objects.filter(
            id=character_event.id,
        ).update(
            status=CharacterEvent.Statuses.PENDING_REVIEW,
            **validated_data,
        )
        transaction.on_commit(
            lambda: send_mail_about_character_event_for_inspector.delay(
                character_event_id=character_event.id,
            ),
        )
        character_event.refresh_from_db()

        return character_event

    def update_from_inspector(
        self,
        character_event: CharacterEvent,
        validated_data: dict[str, Any],
    ) -> CharacterEvent:
        """
        Создание покупки пользователя.
        """
        CharacterEvent.objects.filter(
            id=character_event.id,
        ).update(
            final_status_datetime=(
                timezone.now() if validated_data["status"] == CharacterEvent.Statuses.COMPLETED else None
            ),
            **validated_data,
        )
        character_event = (
            CharacterEvent.objects.select_related(
                "inspector",
                "character__user",
                "event",
                "character__game_world",
            )
            .prefetch_related(
                "event__artifacts",
                "event__event_artifacts",
                "event__competencies",
                "event__event_competencies",
            )
            .get(id=character_event.id)
        )
        character = character_event.character
        if character_event.status == CharacterEvent.Statuses.COMPLETED:
            self.action_post_event_completed(
                character=character,
                character_event=character_event,
            )
        else:
            ActivityLog.objects.create(
                character=character,
                text=_(f"По событию {character_event.event} требуются доработки."),
                content_object=character_event,
            )
        transaction.on_commit(
            lambda: send_mail_about_character_event_for_character.delay(
                character_event_id=character_event.id,
            ),
        )
        return character_event


character_event_service = CharacterEventService()
