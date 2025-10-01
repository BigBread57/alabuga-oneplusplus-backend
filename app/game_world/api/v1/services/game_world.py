import json
from collections import defaultdict
from itertools import chain
from typing import Any
from uuid import UUID

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models, transaction
from django.db.models.functions import DenseRank
from django.utils.translation import gettext_lazy as _
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from common.constants import FieldNameForGenerate, GenerateObjectType
from common.services import BaseService
from game_mechanics.models import Competency, Rank, RequiredRankCompetency
from game_world.api.v1.services.sructure_data_for_generate import GameDataModel
from game_world.models import (
    ActivityCategory,
    Artifact,
    Event,
    EventArtifact,
    EventCompetency,
    GameWorld,
    GameWorldStory,
    Mission,
    MissionArtifact,
    MissionBranch,
    MissionCompetency,
    MissionLevel,
)
from user.models import Character, CharacterMission, CharacterMissionBranch

llm = OpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = llm
Settings.embed_model = embed_model


class GameWorldService(BaseService):
    """
    Игровой мир. Сервис.
    """

    @staticmethod
    def get_content_for_model(game_world: GameWorld, validated_data: dict[str, Any]) -> str:
        """
        Получить контекст для модели.
        """
        content_type_info = {content_type.model: content_type.id for content_type in ContentType.objects.all()}
        # Из поля в GameWorldGenerateSerializer получаем названия модели.
        generate_type_info = {
            name_field.replace("_generate_type", "").replace("_", " ").title().replace(" ", ""): value
            for name_field, value in validated_data.items()
            if name_field.find("_generate_type") >= 0
        }
        # Получаем количество объектов для создания.
        generate_number_info = {
            name_field.replace("_number", "").replace("_", " ").title().replace(" ", ""): value
            for name_field, value in validated_data.items()
            if name_field.find("_number") >= 0
        }
        content = (
            f"Необходимо сформировать объекты для игрового мира {game_world.name}\n (uuid={game_world.uuid})"
            f"{game_world.description}\n\n"
            "Все объекты должны соответствовать этому сеттингу и быть основаны на реальных трудовых "
            "компетенциях и событиях. Общие правила генерации. Все описания реальны, но стилизованы под игровой мир. "
            "Компетенции, события, миссии и артефакты должны быть выполнимыми в реальной профессиональной деятельности."
            "Существующие объекты, которые необходимо использовать при генерации:\n"
        )

        for model_for_default_use in [RequiredRankCompetency, ActivityCategory, MissionLevel]:

            all_fields = [
                field.name
                for field in model_for_default_use._meta.get_fields()
                if isinstance(field, models.Field)
                and field.name
                not in [
                    "color",
                    "icon",
                    "image",
                    "content_object",
                    "created_at",
                    "updated_at",
                ]
            ]
            queryset = list(model_for_default_use.objects.all().values(*all_fields))
            content += f"{json.dumps(queryset, cls=DjangoJSONEncoder, indent=2, ensure_ascii=False)}\n"

        content += "Задача: Сгенерировать JSON-объекты для следующих сущностей:\n"
        # Идем по моделям, дял которых нужно что-то сформировать и создаем content.
        for app_config in {
            apps.get_app_config(app_label="game_mechanics"),
            apps.get_app_config(app_label="game_world"),
        }:
            for model in app_config.get_models():
                if model.__name__ in generate_type_info.keys():
                    generate_object_type = getattr(
                        GenerateObjectType,
                        generate_type_info.get(model.__name__).upper(),
                    )
                    # Указываем модель, тип генерации из GenerateObjectType и поля.
                    content += (
                        f"Для {model.__name__} необходимо {generate_object_type.label}\n"
                        f"Количество: {generate_number_info.get(model.__name__.lower())}\n"
                        f"{model.__doc__}\n\n"
                        f"content_type_id={content_type_info.get(model.__name__.lower())}\n"
                    )
                    for field in model._meta.get_fields():
                        if getattr(field, "help_text", ""):
                            content += f"{field.name} - {str(getattr(field, 'help_text', ''))}\n"

                    # Обогащаем имеющимися данными.
                    if generate_object_type == GenerateObjectType.ADVICE:
                        match model.__name__.lower():
                            case "activitycategory":
                                filters = models.Q()
                            case "missionlevel":
                                filters = models.Q()
                            case "requiredrankcompetency":
                                filters = models.Q(
                                    rank__game_world=game_world,
                                    competency__game_world=game_world,
                                )
                            case "eventartifact":
                                filters = models.Q(
                                    event__game_world=game_world,
                                    artifact__game_world=game_world,
                                )
                            case "eventcompetency":
                                filters = models.Q(
                                    event__game_world=game_world,
                                    competency__game_world=game_world,
                                )
                            case "missionartifact":
                                filters = models.Q(
                                    mission__game_world=game_world,
                                    artifact__game_world=game_world,
                                )
                            case "missioncompetency":
                                filters = models.Q(
                                    mission__game_world=game_world,
                                    competency__game_world=game_world,
                                )
                            case _:
                                filters = models.Q(game_world=game_world)

                        all_fields = [
                            field.name
                            for field in model._meta.get_fields()
                            if isinstance(field, models.Field)
                            and field.name
                            not in [
                                "color",
                                "icon",
                                "image",
                                "content_object",
                                "created_at",
                                "updated_at",
                            ]
                        ]

                        queryset = list(model.objects.filter(filters).values(*all_fields))
                        content += (
                            "Существующие объекты:\n"
                            f"{json.dumps(queryset, cls=DjangoJSONEncoder, indent=2, ensure_ascii=False)}\n"
                        )

        return content

    @staticmethod
    def global_rating(
        game_world: GameWorld,
    ) -> dict[str, Any]:
        """
        Игровой мир. Рейтинг.
        """

    @staticmethod
    def statistics(
        game_world: GameWorld,
    ) -> dict[str, Any]:
        """
        Игровой мир. Статистика.
        """
        mission_branches = defaultdict(list)
        number_mission_branches = defaultdict(int)

        for character_mission_branch in (
            CharacterMissionBranch.objects.select_related(
                "branch",
            )
            .filter(
                branch__is_active=True,
                branch__game_world=game_world,
            )
            .annotate(
                total_missions=models.Count("branch__missions", distinct=True),
                completed_character_missions=models.Count(
                    "character_missions",
                    filter=models.Q(
                        character_missions__status=CharacterMission.Statuses.COMPLETED,
                    ),
                    distinct=True,
                ),
            )
            .annotate(
                is_fully_completed=models.Case(
                    models.When(
                        total_missions=models.F("completed_character_missions"),
                        then=True,
                    ),
                    default=False,
                    output_field=models.BooleanField(),
                )
            )
        ):
            number_mission_branches[character_mission_branch.branch.name] += 1
            if not mission_branches.get(character_mission_branch.branch.name, None):
                mission_branches[character_mission_branch.branch.name] = []
            if character_mission_branch.is_fully_completed:
                mission_branches[character_mission_branch.branch.name].append(character_mission_branch)

        missions = Mission.objects.filter(
            is_active=True,
            game_world=game_world,
        ).annotate(
            total_character_missions=models.Count("character_missions", distinct=True),
            completed_character_missions=models.Count(
                "character_missions",
                filter=models.Q(character_missions__status=CharacterMission.Statuses.COMPLETED),
                distinct=True,
            ),
        )

        completed_or_failed_character_missions = [
            [
                {
                    "date": character_mission["final_status_date"],
                    "value": character_mission["completed"],
                    "type": "Выполнено",
                },
                {
                    "date": character_mission["final_status_date"],
                    "value": character_mission["failed"],
                    "type": "Провалено",
                },
            ]
            for character_mission in CharacterMission.objects.filter(
                status__in={
                    CharacterMission.Statuses.COMPLETED,
                    CharacterMission.Statuses.FAILED,
                },
            )
            .values(
                "final_status_datetime__date",
            )
            .annotate(
                final_status_date=models.F("final_status_datetime__date"),
                completed=models.Count("id", filter=models.Q(status=CharacterMission.Statuses.COMPLETED)),
                failed=models.Count("id", filter=models.Q(status=CharacterMission.Statuses.FAILED)),
            )
        ]

        characters = (
            Character.objects.select_related("user")
            .annotate(
                character_missions_number=models.Count("character_missions", distinct=True),
                character_events_number=models.Count("character_events", distinct=True),
                character_artifacts_number=models.Count("character_artifacts", distinct=True),
                character_competencies_number=models.Count("character_competencies", distinct=True),
            )
            .annotate(
                character_missions_place=models.Window(
                    expression=DenseRank(),
                    order_by=models.F("character_missions_number").desc(),
                ),
                character_events_place=models.Window(
                    expression=DenseRank(),
                    order_by=models.F("character_events_number").desc(),
                ),
                character_artifacts_place=models.Window(
                    expression=DenseRank(),
                    order_by=models.F("character_artifacts_number").desc(),
                ),
                character_competencies_place=models.Window(
                    expression=DenseRank(),
                    order_by=models.F("character_competencies_number").desc(),
                ),
            )
        )

        return {
            "top_characters": [
                {
                    "character_missions_place": character.character_missions_place,
                    "character_missions_number": character.character_missions_number,
                    "character_events_place": character.character_events_place,
                    "character_events_number": character.character_events_number,
                    "character_artifacts_place": character.character_artifacts_place,
                    "character_artifacts_number": character.character_artifacts_number,
                    "character_competencies_place": character.character_competencies_place,
                    "character_competencies_number": character.character_competencies_number,
                    "character_name": character.user.full_name,
                }
                for character in characters
            ],
            "grouping_character_by_ranks": [
                {"name": rank.name, "star": rank.characters_number}
                for rank in Rank.objects.filter(game_world=game_world)
                .annotate(
                    characters_number=models.Count("characters"),
                )
                .order_by("-parent")
            ],
            "number_of_character_who_closed_the_mission_branch": [
                {
                    "letter": mission_branch_name,
                    "frequency": (
                        len(character_mission_branches) / number_mission_branches[mission_branch_name]
                        if len(character_mission_branches) > 0
                        else 0
                    ),
                }
                for mission_branch_name, character_mission_branches in mission_branches.items()
            ],
            "number_of_character_who_closed_the_mission": [
                {
                    "letter": mission.name,
                    "frequency": (
                        mission.completed_character_missions / mission.total_character_missions
                        if mission.completed_character_missions > 0
                        else 0
                    ),
                }
                for mission in missions
            ],
            "completed_or_failed_character_missions": list(chain(*completed_or_failed_character_missions)),
        }

    @staticmethod
    def info_for_generate() -> list[dict[str, Any]]:
        return [
            {
                "field_name": FieldNameForGenerate.RANK_GENERATE_TYPE,
                "description": _("Генерация рангов"),
            },
            {
                "field_name": FieldNameForGenerate.COMPETENCY_GENERATE_TYPE,
                "description": _("Генерация компетенций"),
            },
            # {
            #     "field_name": FieldNameForGenerate.REQUIRED_RANK_COMPETENCY_GENERATE_TYPE,
            #     "description": _(
            #         "Генерация взаимосвязи ранга и компетенций (какие компетенции нужны, чтобы получить новый ранг)"
            #     ),
            # },
            # {
            #     "field_name": FieldNameForGenerate.ACTIVITY_CATEGORY_GENERATE_TYPE,
            #     "description": _("Генерация категорий миссии и событий (квесты, лектории и др.)"),
            # },
            {
                "field_name": FieldNameForGenerate.ARTIFACT_GENERATE_TYPE,
                "description": _("Генерация артефактов"),
            },
            {
                "field_name": FieldNameForGenerate.EVENT_GENERATE_TYPE,
                "description": _("Генерация событий (задание, которое распространяется на всех одновременно)"),
            },
            # {
            #     "field_name": FieldNameForGenerate.EVENT_ARTIFACT_GENERATE_TYPE,
            #     "description": _("Генерация артефактов, которые можно получить за выполнение события"),
            # },
            {
                "field_name": FieldNameForGenerate.EVENT_COMPETENCY_GENERATE_TYPE,
                "description": _("Генерация компетенций, которые прокачиваются за выполнение события"),
            },
            {
                "field_name": FieldNameForGenerate.GAME_WORLD_STORY_GENERATE_TYPE,
                "description": _("Генерация веток миссий"),
            },
            {
                "field_name": FieldNameForGenerate.MISSION_GENERATE_TYPE,
                "description": _(
                    "Генерация уровней миссий (от уровня зависит получаемый опыт и валют, например: "
                    "легкая, сложная и др.)"
                ),
            },
            # {
            #     "field_name": FieldNameForGenerate.MISSION_ARTIFACT_GENERATE_TYPE,
            #     "description": _("Генерация миссий"),
            # },
            {
                "field_name": FieldNameForGenerate.MISSION_COMPETENCY_GENERATE_TYPE,
                "description": _("Генерация миссий"),
            },
            {
                "field_name": FieldNameForGenerate.MISSION_BRANCH_GENERATE_TYPE,
                "description": _("Генерация артефактов, которые можно получить за выполнение миссии"),
            },
            # {
            #     "field_name": FieldNameForGenerate.MISSION_LEVEL_GENERATE_TYPE,
            #     "description": _("Генерация компетенций, которые прокачиваются за выполнение миссии"),
            # },
        ]

    @staticmethod
    def transform_ai_response_to_dict(ai_data):
        """Преобразует данные от ИИ в словарь для GameDataModel"""
        result = {}
        for section_name, items in ai_data:
            transformed_items = []
            for item in items:
                item_dict = {}
                for key, value in item:
                    item_dict[key] = value
                transformed_items.append(item_dict)
            result[section_name] = transformed_items
        return result

    def generate(
        self,
        game_world: GameWorld,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Игровой мир. Генерация.
        """
        # prompt = content=self.get_content_for_model(
        #     game_world=game_world,
        #     validated_data=validated_data,
        # )
        game_data = (
            llm.as_structured_llm(output_cls=GameDataModel)
            .complete(prompt="Сформируй мне по 1 объекту для класса, переданного в output_cls")
            .raw
        )
        transformed_game_data = self.transform_ai_response_to_dict(game_data)
        return GameDataModel(**transformed_game_data).model_dump()


    def update_or_create_all_entities(self, game_world_data: dict[str, Any], cells_data: dict[str, Any]):
        """
        Обновляет существующие сущности в БД или создает новые на основе данных графа
        """
        # Словари для хранения соответствий UUID и ID сущностей
        uuid_to_id_map = {}

        # Обрабатываем клетки графа
        for cell in cells_data.get("cells", []):
            cell_id = cell.get("id")
            cell_type = cell.get("data", {}).get("type")

            if not cell_id or not cell_type:
                continue

            # Обрабатываем разные типы сущностей
            if cell_type == "rank":
                self._process_rank(cell, game_world_data, uuid_to_id_map)
            elif cell_type == "missionBranch":
                self._process_mission_branch(cell, game_world_data, uuid_to_id_map)
            elif cell_type == "mission":
                self._process_mission(cell, game_world_data, uuid_to_id_map)
            elif cell_type == "artefact":
                self._process_artifact(cell, game_world_data, uuid_to_id_map)
            elif cell_type == "event":
                self._process_event(cell, game_world_data, uuid_to_id_map)
            elif cell_type == "competency":
                self._process_competency(cell, game_world_data, uuid_to_id_map)

        # Обрабатываем связи после создания всех сущностей
        self._process_relationships(cells_data, uuid_to_id_map)

    def _process_rank(self, cell, game_world_data, uuid_to_id_map):
        """Обрабатывает ранг"""
        rank_data = cell["data"]
        uuid = cell["id"]

        # Ищем ранг в исходных данных
        original_rank = self._find_entity_by_uuid(game_world_data["ranks"], uuid)

        rank_data_to_save = {
            "uuid": uuid,
            "name": rank_data["name"],
            "description": rank_data["description"],
            "required_experience": rank_data["required_experience"],
            "color": rank_data["color"],
            "x": cell.get("x", 0),
            "y": cell.get("y", 0)
        }

        if original_rank:
            # Обновляем существующий ранг
            rank_id = self._update_rank(original_rank["id"], rank_data_to_save)
        else:
            # Создаем новый ранг
            rank_id = self._create_rank(rank_data_to_save)

        uuid_to_id_map[f"rank-{uuid}"] = rank_id

    def _process_mission_branch(self, cell, game_world_data, uuid_to_id_map):
        """Обрабатывает ветку миссий"""
        branch_data = cell["data"]
        uuid = cell["id"]

        # Ищем ветку в исходных данных
        original_branch = None
        for rank in game_world_data["ranks"]:
            original_branch = self._find_entity_by_uuid(rank.get("mission_branches", []), uuid)
            if original_branch:
                break

        branch_data_to_save = {
            "uuid": uuid,
            "name": branch_data["name"],
            "description": branch_data["description"],
            "category_name": branch_data["category"],
            "time_to_complete": branch_data["time_to_complete"],
            "x": cell.get("x", 0),
            "y": cell.get("y", 0)
        }

        if original_branch:
            branch_id = self._update_mission_branch(original_branch["id"], branch_data_to_save)
        else:
            branch_id = self._create_mission_branch(branch_data_to_save)

        uuid_to_id_map[f"mission-branch-{uuid}"] = branch_id

    def _process_mission(self, cell, game_world_data, uuid_to_id_map):
        """Обрабатывает миссию"""
        mission_data = cell["data"]
        uuid = cell["id"]

        # Ищем миссию в исходных данных
        original_mission = None
        for rank in game_world_data["ranks"]:
            for branch in rank.get("mission_branches", []):
                original_mission = self._find_entity_by_uuid(branch.get("missions", []), uuid)
                if original_mission:
                    break
            if original_mission:
                break

        mission_data_to_save = {
            "uuid": uuid,
            "name": mission_data["name"],
            "description": mission_data["description"],
            "experience": mission_data["experience"],
            "currency": mission_data["currency"],
            "level_name": mission_data["level"],
            "is_key_mission": mission_data["is_key_mission"],
            "time_to_complete": mission_data.get("time_to_complete", 0),
            "order": mission_data.get("order", 0),
            "x": cell.get("x", 0),
            "y": cell.get("y", 0)
        }

        if original_mission:
            mission_id = self._update_mission(original_mission["id"], mission_data_to_save)
        else:
            mission_id = self._create_mission(mission_data_to_save)

        uuid_to_id_map[f"mission-{uuid}"] = mission_id

    def _process_artifact(self, cell, game_world_data, uuid_to_id_map):
        """Обрабатывает артефакт"""
        artifact_data = cell["data"]
        uuid = cell["id"]

        # Ищем артефакт в исходных данных
        original_artifact = self._find_artifact_in_data(game_world_data, uuid)

        artifact_data_to_save = {
            "uuid": uuid,
            "name": artifact_data["name"],
            "description": artifact_data["description"],
            "modifier": artifact_data["modifier"],
            "modifier_value": artifact_data["modifier_value"],
            "color": artifact_data.get("color", ""),
            "x": cell.get("x", 0),
            "y": cell.get("y", 0)
        }

        if original_artifact:
            artifact_id = self._update_artifact(original_artifact["id"], artifact_data_to_save)
        else:
            artifact_id = self._create_artifact(artifact_data_to_save)

        uuid_to_id_map[f"artifact-{uuid}"] = artifact_id

    def _process_event(self, cell, game_world_data, uuid_to_id_map):
        """Обрабатывает событие"""
        event_data = cell["data"]
        uuid = cell["id"]

        # Ищем событие в исходных данных
        original_event = None
        for rank in game_world_data["ranks"]:
            original_event = self._find_entity_by_uuid(rank.get("events", []), uuid)
            if original_event:
                break

        event_data_to_save = {
            "uuid": uuid,
            "name": event_data["name"],
            "description": event_data["description"],
            "experience": event_data["experience"],
            "currency": event_data["currency"],
            "category_name": event_data["category"],
            "required_number": event_data["required_number"],
            "is_active": event_data.get("is_active", True),
            "start_datetime": event_data.get("start_datetime"),
            "time_to_complete": event_data.get("time_to_complete", 0),
            "x": cell.get("x", 0),
            "y": cell.get("y", 0)
        }

        if original_event:
            event_id = self._update_event(original_event["id"], event_data_to_save)
        else:
            event_id = self._create_event(event_data_to_save)

        uuid_to_id_map[f"event-{uuid}"] = event_id

    def _process_competency(self, cell, game_world_data, uuid_to_id_map):
        """Обрабатывает компетенцию"""
        competency_data = cell["data"]
        uuid = cell["id"]

        # Ищем компетенцию в исходных данных
        original_competency = self._find_competency_in_data(game_world_data, uuid)

        competency_data_to_save = {
            "uuid": uuid,
            "name": competency_data["name"],
            "description": competency_data["description"],
            "level": competency_data["level"],
            "required_experience": competency_data["required_experience"],
            "color": competency_data["color"],
            "x": cell.get("x", 0),
            "y": cell.get("y", 0)
        }

        if original_competency:
            competency_id = self._update_competency(original_competency["id"], competency_data_to_save)
        else:
            competency_id = self._create_competency(competency_data_to_save)

        uuid_to_id_map[f"competency-{uuid}"] = competency_id

    def _process_relationships(self, cells_data, uuid_to_id_map):
        """Обрабатывает связи между сущностями"""
        for cell in cells_data.get("cells", []):
            if cell.get("shape") == "entity-edge":
                self._process_edge_relationship(cell, uuid_to_id_map)

    def _process_edge_relationship(self, edge, uuid_to_id_map):
        """Обрабатывает связь между двумя сущностями"""
        source_cell = edge.get("source", {}).get("cell", "")
        target_cell = edge.get("target", {}).get("cell", "")

        if not source_cell or not target_cell:
            return

        # Получаем ID сущностей из маппинга
        source_id = uuid_to_id_map.get(source_cell)
        target_id = uuid_to_id_map.get(target_cell)

        if not source_id or not target_id:
            return

        # Определяем тип связи и создаем/обновляем ее
        self._create_or_update_relationship(source_cell, target_cell, source_id, target_id)

    def _find_entity_by_uuid(self, entities_list, uuid):
        """Ищет сущность по UUID в списке"""
        if not entities_list:
            return None
        return next((entity for entity in entities_list if entity.get("uuid") == uuid), None)

    def _find_artifact_in_data(self, game_world_data, uuid):
        """Ищет артефакт по UUID во всех сущностях"""
        # Ищем в миссиях
        for rank in game_world_data["ranks"]:
            for branch in rank.get("mission_branches", []):
                for mission in branch.get("missions", []):
                    artifact = self._find_entity_by_uuid(mission.get("artifacts", []), uuid)
                    if artifact:
                        return artifact

        # Ищем в событиях
        for rank in game_world_data["ranks"]:
            for event in rank.get("events", []):
                artifact = self._find_entity_by_uuid(event.get("artifacts", []), uuid)
                if artifact:
                    return artifact

        return None

    def _find_competency_in_data(self, game_world_data, uuid):
        """Ищет компетенцию по UUID во всех сущностях"""
        # Ищем в миссиях
        for rank in game_world_data["ranks"]:
            for branch in rank.get("mission_branches", []):
                for mission in branch.get("missions", []):
                    competency = self._find_entity_by_uuid(mission.get("competencies", []), uuid)
                    if competency:
                        return competency

        # Ищем в событиях
        for rank in game_world_data["ranks"]:
            for event in rank.get("events", []):
                competency = self._find_entity_by_uuid(event.get("competencies", []), uuid)
                if competency:
                    return competency

        # Ищем в required_rank_competencies
        for rank in game_world_data["ranks"]:
            competency = self._find_entity_by_uuid(rank.get("required_rank_competencies", []), uuid)
            if competency:
                return competency

        return None

    # Методы для работы с БД (заглушки - нужно реализовать под вашу ORM)
    def _update_rank(self, rank_id, data):
        """Обновляет ранг в БД"""
        # Реализация обновления ранга
        return rank_id

    def _create_rank(self, data):
        """Создает новый ранг в БД"""
        # Реализация создания ранга
        return 1  # возвращаем новый ID

    def _update_mission_branch(self, branch_id, data):
        """Обновляет ветку миссий в БД"""
        # Реализация обновления ветки миссий
        return branch_id

    def _create_mission_branch(self, data):
        """Создает новую ветку миссий в БД"""
        # Реализация создания ветки миссий
        return 1  # возвращаем новый ID

    # Аналогичные методы для других сущностей...
    def _update_mission(self, mission_id, data):
        return mission_id

    def _create_mission(self, data):
        return 1

    def _update_artifact(self, artifact_id, data):
        return artifact_id

    def _create_artifact(self, data):
        return 1

    def _update_event(self, event_id, data):
        return event_id

    def _create_event(self, data):
        return 1

    def _update_competency(self, competency_id, data):
        return competency_id

    def _create_competency(self, data):
        return 1

    def _create_or_update_relationship(self, source_type, target_type, source_id, target_id):
        """Создает или обновляет связь между сущностями"""
        # Реализация создания/обновления связей в БД
        # В зависимости от source_type и target_type определяем тип связи
        # и создаем соответствующую запись в таблице связей
        pass






    def get_data_for_graph(self, game_world_data: dict[str, Any], data_for_graph: dict[str, Any] | None = None):
        """
        Преобразует объект игрового мира в формат cells для визуализации графа
        """
        cells = []

        # Конфигурируемые параметры для позиционирования
        config = {
            "rank_height": 300,  # расстояние между рангами по вертикали
            "mission_branch_height": 120,  # расстояние между ветками миссий
            "mission_height": 150,  # расстояние между миссиями
            "artifact_height": 80,  # расстояние между артефактами
            "event_height": 100,  # расстояние между событиями
            "competency_height": 70,  # расстояние между компетенциями
            "node_width": 250,  # ширина узла
            "node_height": 80,  # высота узла
            "horizontal_spacing": 260,  # горизонтальное расстояние между узлами
            "initial_x": 300,  # начальная позиция по X для рангов
            "initial_y": 50,  # начальная позиция по Y для первого ранга
        }

        def get_coordinates_from_data(node_id, default_x, default_y):
            """
            Функция для получения координат из data_for_graph.
            """
            if data_for_graph and "cells" in data_for_graph:
                for cell in data_for_graph["cells"]:
                    if cell.get("id") == node_id and "x" in cell and "y" in cell:
                        return cell["x"], cell["y"]
            return default_x, default_y

        # Обрабатываем ранги
        for rank in game_world_data.get("ranks", []):
            # Создаем узел ранга
            rank_id = rank['uuid']
            default_rank_y = config["initial_y"] + (rank["id"] - 1) * config["rank_height"]
            rank_x, rank_y = get_coordinates_from_data(rank_id, config["initial_x"], default_rank_y)

            rank_node = {
                "id": rank_id,
                "shape": "rank|node",
                "x": rank_x,
                "y": rank_y,
                "attrs": {
                    "title": {"text": rank["name"]},
                    "description": {"text": rank["description"]},
                },
                "data": {
                    "type": "rank",
                    "name": rank.get("name"),
                    "description": rank.get("description", ""),
                    "required_experience": rank.get("required_experience"),
                    "icon": rank.get("icon", ""),
                    "color": rank.get("color", ""),
                    "parent": rank.get("parent", None),
                        "game_world": mission_branch.get("game_world"),
                },
            }
            cells.append(rank_node)
            if rank.get("parent"):
                edge = {
                    "id": f"{rank['uuid']}|{rank['parent']['uuid']}",
                    "shape": "rank|rank|edge",
                    "source": {"cell": rank['uuid']},
                    "target": {"cell": rank['parent']['uuid']}
                }
                cells.append(edge)

            # Переменные для отслеживания максимальной высоты элементов ранга
            max_mission_branch_y = rank_y
            max_artifact_y = rank_y
            max_competency_y = rank_y

            # Обрабатываем ветки миссий для этого ранга
            mission_branch_y = rank_y + config["mission_branch_height"]
            for mission_branch in rank.get("mission_branches", []):
                mission_branch_id = mission_branch['uuid']
                default_mission_branch_x = 150 + (mission_branch["id"] - 1) * config["horizontal_spacing"]
                mission_branch_x, mission_branch_y = get_coordinates_from_data(
                    mission_branch_id, default_mission_branch_x, mission_branch_y,
                )

                mission_branch_node = {
                    "id": mission_branch_id,
                    "shape": "missionbranch|node",
                    "x": mission_branch_x,
                    "y": mission_branch_y,
                    "attrs": {
                        "title": {"text": mission_branch["name"]},
                        "description": {"text": mission_branch["description"]},
                    },
                    "data": {
                        "type": "missionBranch",
                        "name": mission_branch.get("name"),
                        "description": mission_branch.get("description", ""),
                        "icon": mission_branch.get("icon", ""),
                        "color": mission_branch.get("color", ""),
                        "is_active": mission_branch.get("is_active"),
                        "start_datetime": mission_branch.get("start_datetime", None),
                        "time_to_complete": mission_branch.get("time_to_complete", None),
                        "rank": mission_branch.get("rank"),
                        "category": mission_branch.get("category"),
                        "mentor": mission_branch.get("mentor"),
                        "game_world": mission_branch.get("game_world"),
                    },
                }
                cells.append(mission_branch_node)

                # Создаем связь от ранга к ветке миссий
                edge = {
                    "id": f"{rank['uuid']}|{mission_branch['uuid']}",
                    "shape": "rank|missionbranch|edge",
                    "source": {"cell": rank['uuid']},
                    "target": {"cell": mission_branch['uuid']}
                }
                cells.append(edge)

                # Обрабатываем миссии в этой ветке
                mission_y = mission_branch_y + config["mission_height"]
                for mission in mission_branch.get("missions", []):
                    mission_id = mission['uuid']
                    default_mission_x = 100 + (mission["id"] - 1) * config["horizontal_spacing"]
                    mission_x, mission_y = get_coordinates_from_data(mission_id, default_mission_x, mission_y)

                    mission_node = {
                        "id": mission_id,
                        "shape": "mission|node",
                        "x": mission_x,
                        "y": mission_y,
                        "attrs": {
                            "title": {"text": mission["name"]},
                            "description": {"text": f"Опыт: {mission['experience']}, Валюта: {mission['currency']}"},
                        },
                        "data": {
                            "type": "mission",
                            "name": mission["name"],
                            "description": f"Опыт: {mission['experience']}, Валюта: {mission['currency']}",
                            "experience": mission["experience"],
                            "currency": mission["currency"],
                            "level": mission["level"]["name"],
                            "is_key_mission": mission["is_key_mission"],
                        },
                    }
                    cells.append(mission_node)

                    # Создаем связь от ветки миссий к миссии
                    edge = {
                        "id": f"{mission_branch['uuid']}|{mission['uuid']}",
                        "shape": "missionbranch|mission|edge",
                        "source": {"cell": mission_branch['uuid']},
                        "target": {"cell": mission['uuid']},
                    }
                    cells.append(edge)

                    # Обрабатываем артефакты для этой миссии
                    artifact_y = mission_y + config["artifact_height"]
                    for artifact in mission.get("artifacts", []):
                        artifact_id = artifact['uuid']
                        default_artifact_x = 100 + (artifact["id"] - 1) * config["horizontal_spacing"]
                        artifact_x, artifact_y = get_coordinates_from_data(artifact_id, default_artifact_x, artifact_y)

                        artifact_node = {
                            "id": artifact_id,
                            "shape": "artefact|node",
                            "x": artifact_x,
                            "y": artifact_y,
                            "attrs": {
                                "title": {"text": artifact["name"]},
                                "description": {"text": artifact["description"]},
                            },
                            "data": {
                                "type": "artefact",
                                "name": artifact["name"],
                                "description": artifact["description"],
                                "modifier": artifact["modifier"],
                                "modifier_value": artifact["modifier_value"],
                            },
                        }
                        cells.append(artifact_node)

                        # Создаем связь от миссии к артефакту
                        edge = {
                            "id": f"{mission['uuid']}|{artifact['uuid']}",
                            "shape": "mission|artifact|edge",
                            "source": {"cell": mission['uuid']},
                            "target": {"cell": artifact['uuid']}
                        }
                        cells.append(edge)

                        # Обновляем максимальную высоту артефактов
                        max_artifact_y = max(max_artifact_y, artifact_y)
                        artifact_y += config["artifact_height"]

                    # Обрабатываем компетенции для этой миссии
                    competency_y = mission_y + config["competency_height"]
                    for competency in mission.get("competencies", []):
                        competency_id = competency['uuid']
                        default_competency_x = 100 + (competency["id"] - 1) * config["horizontal_spacing"]
                        competency_x, competency_y = get_coordinates_from_data(competency_id, default_competency_x,
                                                                               competency_y)

                        competency_node = {
                            "id": competency_id,
                            "shape": "competency|node",
                            "x": competency_x,
                            "y": competency_y,
                            "attrs": {
                                "title": {"text": competency["name"]},
                                "description": {"text": competency["description"]},
                            },
                            "data": {
                                "type": "competency",
                                "name": competency["name"],
                                "description": competency["description"],
                                "level": competency["level"],
                                "required_experience": competency["required_experience"],
                                "color": competency["color"],
                            },
                        }
                        cells.append(competency_node)

                        # Создаем связь от миссии к компетенции
                        edge = {
                            "id": f"{mission['uuid']}|{competency['uuid']}",
                            "shape": "mission|competency",
                            "source": {"cell": mission['uuid']},
                            "target": {"cell": competency['uuid']},
                        }
                        cells.append(edge)

                        # Обновляем максимальную высоту компетенций
                        max_competency_y = max(max_competency_y, competency_y)
                        competency_y += config["competency_height"]

                    # Обновляем максимальную высоту миссий
                    max_mission_branch_y = max(max_mission_branch_y, mission_y)

                mission_branch_y += config["mission_branch_height"]

            # Рассчитываем позицию для событий на основе максимальной высоты элементов
            # Используем максимальную высоту из артефактов, веток миссий или компетенций
            max_element_height = max(max_mission_branch_y, max_artifact_y, max_competency_y)
            event_y = max_element_height + config["event_height"]

            # Обрабатываем события для этого ранга
            for event in rank.get("events", []):
                event_id = event['uuid']
                event_x, event_y = get_coordinates_from_data(event_id, config["initial_x"], event_y)

                event_node = {
                    "id": event_id,
                    "shape": "event|node",
                    "x": event_x,
                    "y": event_y,
                    "attrs": {
                        "title": {"text": event["name"]},
                        "description": {"text": event["description"]},
                    },
                    "data": {
                        "type": "event",
                        "name": event["name"],
                        "description": event["description"],
                        "experience": event["experience"],
                        "currency": event["currency"],
                        "category": event["category"]["name"],
                        "required_number": event["required_number"],
                    },
                }
                cells.append(event_node)

                # Обрабатываем компетенции для этого события
                event_competency_y = event_y + config["competency_height"]
                for competency in event.get("competencies", []):
                    competency_id = competency['uuid']
                    default_competency_x = 100 + (competency["id"] - 1) * config["horizontal_spacing"]
                    competency_x, event_competency_y = get_coordinates_from_data(competency_id, default_competency_x,
                                                                                 event_competency_y)

                    competency_node = {
                        "id": competency_id,
                        "shape": "competency|node",
                        "x": competency_x,
                        "y": event_competency_y,
                        "attrs": {
                            "title": {"text": competency["name"]},
                            "description": {"text": competency["description"]},
                        },
                        "data": {
                            "type": "competency",
                            "name": competency["name"],
                            "description": competency["description"],
                            "level": competency["level"],
                            "required_experience": competency["required_experience"],
                            "color": competency["color"],
                        },
                    }
                    cells.append(competency_node)

                    # Создаем связь от события к компетенции
                    edge = {
                        "id": f"{event['uuid']}-{competency['uuid']}",
                        "shape": "event|competency|edge",
                        "source": {"cell": event['uuid']},
                        "target": {"cell": competency['uuid']},
                    }
                    cells.append(edge)

                    event_competency_y += config["competency_height"]

                # Обрабатываем артефакты для этого события
                event_artifact_y = event_y + config["artifact_height"]
                for artifact in event.get("artifacts", []):
                    artifact_id = artifact['uuid']
                    default_artifact_x = 100 + (artifact["id"] - 1) * config["horizontal_spacing"]
                    artifact_x, event_artifact_y = get_coordinates_from_data(artifact_id, default_artifact_x,
                                                                             event_artifact_y)

                    artifact_node = {
                        "id": artifact_id,
                        "shape": "artefact|node",
                        "x": artifact_x,
                        "y": event_artifact_y,
                        "attrs": {
                            "title": {"text": artifact["name"]},
                            "description": {"text": artifact["description"]},
                        },
                        "data": {
                            "type": "artefact",
                            "name": artifact["name"],
                            "description": artifact["description"],
                            "modifier": artifact["modifier"],
                            "modifier_value": artifact["modifier_value"],
                        },
                    }
                    cells.append(artifact_node)

                    # Создаем связь от события к артефакту
                    edge = {
                        "id": f"{event['uuid']}|{artifact['uuid']}",
                        "shape": "event|artifact|edge",
                        "source": {"cell": event['uuid']},
                        "target": {"cell": artifact['uuid']},
                    }
                    cells.append(edge)

                    event_artifact_y += config["artifact_height"]

                # Создаем связи от всех артефактов к событию
                for mission_branch in rank.get("mission_branches", []):
                    for mission in mission_branch.get("missions", []):
                        for artifact in mission.get("artifacts", []):
                            edge = {
                                "id": f"{artifact['uuid']}|{event['uuid']}",
                                "shape": "artifact|event|edge",
                                "source": {"cell": artifact['uuid']},
                                "target": {"cell": event['uuid']},
                            }
                            cells.append(edge)

                # Также создаем связь от ранга к событию
                edge = {
                    "id": f"{rank['uuid']}-{event['uuid']}",
                    "shape": "rank|event|edge",
                    "source": {"cell": rank['uuid']},
                    "target": {"cell": event['uuid']},
                }
                cells.append(edge)

                event_y += config["event_height"]

            # Обновляем расстояние между рангами на основе фактической высоты текущего ранга
            if rank["id"] < len(game_world_data.get("ranks", [])):
                current_rank_height = event_y - rank_y
                config["rank_height"] = max(config["rank_height"], current_rank_height + 50)  # добавляем отступ

        return {"cells": cells}


game_world_service = GameWorldService()
