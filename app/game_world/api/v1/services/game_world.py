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
            "Задача: Сгенерировать JSON-объекты для следующих сущностей:"
        )
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
                        f"content_type_id={content_type_info.get(model.__name__.lower())}"
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
                            f"{json.dumps(queryset, cls=DjangoJSONEncoder, indent=2, ensure_ascii=False)}"
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
                    )
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
            {
                "field_name": FieldNameForGenerate.REQUIRED_RANK_COMPETENCY_GENERATE_TYPE,
                "description": _(
                    "Генерация взаимосвязи ранга и компетенций (какие компетенции нужны, чтобы получить новый ранг)"
                ),
            },
            {
                "field_name": FieldNameForGenerate.ACTIVITY_CATEGORY_GENERATE_TYPE,
                "description": _("Генерация категорий миссии и событий (квесты, лектории и др.)"),
            },
            {
                "field_name": FieldNameForGenerate.ARTIFACT_GENERATE_TYPE,
                "description": _("Генерация артефактов"),
            },
            {
                "field_name": FieldNameForGenerate.EVENT_GENERATE_TYPE,
                "description": _("Генерация событий (задание, которое распространяется на всех одновременно)"),
            },
            {
                "field_name": FieldNameForGenerate.EVENT_ARTIFACT_GENERATE_TYPE,
                "description": _("Генерация артефактов, которые можно получить за выполнение события"),
            },
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
            {
                "field_name": FieldNameForGenerate.MISSION_ARTIFACT_GENERATE_TYPE,
                "description": _("Генерация миссий"),
            },
            {
                "field_name": FieldNameForGenerate.MISSION_COMPETENCY_GENERATE_TYPE,
                "description": _("Генерация миссий"),
            },
            {
                "field_name": FieldNameForGenerate.MISSION_BRANCH_GENERATE_TYPE,
                "description": _("Генерация артефактов, которые можно получить за выполнение миссии"),
            },
            {
                "field_name": FieldNameForGenerate.MISSION_LEVEL_GENERATE_TYPE,
                "description": _("Генерация компетенций, которые прокачиваются за выполнение миссии"),
            },
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

    def create_or_update_entities_optimized(
        self,
        model: models.Model,
        game_world: GameWorld,
        validated_data_for_entities: list[dict[str, Any]],
        maps: dict[str, Any] | None = None,
    ) -> dict[str, int]:
        """
        Еще более оптимизированная версия с предварительной загрузкой всех данных.
        """
        with transaction.atomic():
            # 1. Получаем все существующие объекты одним запросом
            existing_entities = {entity.uuid: entity for entity in model.objects.filter(game_world=game_world)}
            existing_uuids = set(existing_entities.keys())

            # 2. Подготавливаем данные
            entities_for_create = []
            entities_for_update = []
            parent_relationships = {}  # uuid -> parent_uuid

            for validated_data in validated_data_for_entities:
                uuid = validated_data["uuid"]

                # Сохраняем parent связь для последующей обработки
                parent_uuid = validated_data.pop("parent_uuid", None)
                if parent_uuid:
                    parent_relationships[uuid] = parent_uuid

                # Заменяем game_world_uuid на объект
                validated_data["game_world"] = game_world
                validated_data.pop("game_world_uuid", None)

                # Обрабатываем ForeignKey поля через maps
                if maps:
                    for field_name, field_map in maps.items():
                        if field_name in validated_data:
                            uuid_value = validated_data[field_name]
                            if uuid_value in field_map:
                                validated_data[field_name + "_id"] = field_map[uuid_value]
                                validated_data.pop(field_name)
                            else:
                                # Если UUID не найден в маппинге, пропускаем или обрабатываем ошибку
                                validated_data.pop(field_name)
                                # Можно добавить логирование или выбросить исключение
                                # raise ValueError(f"UUID {uuid_value} not found in {field_name} map")

                if uuid not in existing_uuids:
                    entities_for_create.append(model(**validated_data))
                else:
                    # Обновляем существующий объект
                    entity = existing_entities[uuid]
                    for key, value in validated_data.items():
                        if key != "uuid" and getattr(entity, key) != value:
                            setattr(entity, key, value)
                    entities_for_update.append(entity)

            # 3. Выполняем bulk операции
            if entities_for_create:
                created_entities = model.objects.bulk_create(entities_for_create)
                # Добавляем созданные объекты в словарь для parent обработки
                for entity in created_entities:
                    existing_entities[entity.uuid] = entity

            if entities_for_update:
                # Определяем поля для обновления
                update_fields = set()
                for entity in entities_for_update:
                    for field in validated_data_for_entities[0].keys():
                        if field != "uuid":
                            update_fields.add(field)

                model.objects.bulk_update(entities_for_update, list(update_fields))

            # 4. Обрабатываем parent связи
            if parent_relationships:
                self._apply_parent_relationships(existing_entities, parent_relationships)

            # 5. Возвращаем маппинг
            return {str(uuid): entity.id for uuid, entity in existing_entities.items()}

    def _apply_parent_relationships(
        self,
        entities_dict: dict[UUID, models.Model],
        parent_relationships: dict[UUID, UUID],
    ) -> None:
        """
        Применяет parent связи к объектам.
        """
        entities_to_update = []

        for child_uuid, parent_uuid in parent_relationships.items():
            child_entity = entities_dict.get(child_uuid)
            parent_entity = entities_dict.get(parent_uuid)

            if child_entity and parent_entity and child_entity.parent_id != parent_entity.id:
                child_entity.parent = parent_entity
                entities_to_update.append(child_entity)

        if entities_to_update:
            # Используем модель из первого объекта (все объекты одной модели)
            model_type = type(entities_to_update[0])
            model_type.objects.bulk_update(entities_to_update, ["parent"])

    def update_or_create_all_entitys(
        self,
        game_world: GameWorld,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Игровой мир. Генерация.
        """
        with transaction.atomic():
            maps = {
                "mentor": {
                    character.uuid: character.uuid for character in Character.objects.filter(game_world=game_world)
                }
            }
            competencies_map = self.create_or_update_entities(
                model=Competency,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("competencies", []),
            )
            maps.update(competency=competencies_map)
            ranks_map = self.create_or_update_entities(
                model=Rank,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("ranks", []),
            )
            maps.update(rank=ranks_map)
            required_rank_competency_map = self.create_or_update_entities(
                model=RequiredRankCompetency,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("required_rank_competencies", []),
                maps=maps,
            )
            maps.update(required_rank_competency=required_rank_competency_map)
            activity_categories_map = self.create_or_update_entities(
                model=ActivityCategory,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("activity_categories", []),
            )
            maps.update(activity_category=activity_categories_map)
            artifacts_map = self.create_or_update_entities(
                model=Artifact,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("artifacts", []),
            )
            maps.update(artifact=artifacts_map)
            events_map = self.create_or_update_entities(
                model=Event,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("events", []),
            )
            maps.update(event=events_map)
            event_artifacts_map = self.create_or_update_entities(
                model=EventArtifact,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("event_artifacts", []),
            )
            maps.update(event_artifact=event_artifacts_map)
            event_competencies_map = self.create_or_update_entities(
                model=EventCompetency,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("event_competencies", []),
            )
            maps.update(event_competency=event_competencies_map)
            game_world_stories_map = self.create_or_update_entities(
                model=GameWorldStory,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("game_world_stories", []),
            )
            maps.update(game_world_story=game_world_stories_map)
            mission_branches_map = self.create_or_update_entities(
                model=MissionBranch,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("mission_branches", []),
            )
            maps.update(mission_branch=mission_branches_map)
            mission_levels_map = self.create_or_update_entities(
                model=MissionLevel,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("mission_levels", []),
            )
            maps.update(mission_level=mission_levels_map)
            missions_map = self.create_or_update_entities(
                model=Mission,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("missions", []),
            )
            maps.update(mission=missions_map)
            mission_artefacts_map = self.create_or_update_entities(
                model=MissionArtifact,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("mission_artefacts", []),
            )
            maps.update(mission_artefact=mission_artefacts_map)
            mission_competencies_map = self.create_or_update_entities(
                model=MissionCompetency,
                game_world=game_world,
                validated_data_for_entities=validated_data.get("mission_competencies", []),
            )
            maps.update(mission_competency=mission_competencies_map)

    def get_data_for_graph(
            self,
            game_world_data: dict[str, Any],
            data_for_graph: dict[str, Any] | None = None
    ):
        """
        Преобразует объект игрового мира в формат cells для визуализации графа
        """
        cells = []
        edge_counter = 1

        # Конфигурируемые параметры для позиционирования
        config = {
            "rank_height": 300,  # расстояние между рангами по вертикали
            "mission_branch_height": 120,  # расстояние между ветками миссий
            "mission_height": 150,  # расстояние между миссиями
            "artifact_height": 80,  # расстояние между артефактами
            "event_height": 100,  # расстояние между событиями
            "node_width": 250,  # ширина узла
            "node_height": 80,  # высота узла
            "horizontal_spacing": 260,  # горизонтальное расстояние между узлами
            "initial_x": 300,  # начальная позиция по X для рангов
            "initial_y": 50,  # начальная позиция по Y для первого ранга
        }

        # Функция для получения координат из data_for_graph
        def get_coordinates_from_data(node_id, default_x, default_y):
            if data_for_graph and "cells" in data_for_graph:
                for cell in data_for_graph["cells"]:
                    if cell.get("id") == node_id and "x" in cell and "y" in cell:
                        return cell["x"], cell["y"]
            return default_x, default_y

        # Обрабатываем ранги
        for rank in game_world_data.get("ranks", []):
            # Создаем узел ранга
            rank_id = f"rank-{rank['id']}"
            default_rank_y = config["initial_y"] + (rank["id"] - 1) * config["rank_height"]
            rank_x, rank_y = get_coordinates_from_data(rank_id, config["initial_x"], default_rank_y)

            rank_node = {
                "id": rank_id,
                "shape": "rank-node",
                "x": rank_x,
                "y": rank_y,
                "attrs": {
                    "title": {"text": rank["name"]},
                    "description": {"text": rank["description"]},
                },
                "data": {
                    "type": "rank",
                    "name": rank["name"],
                    "description": rank["description"],
                    "required_experience": rank["required_experience"],
                    "color": rank["color"],
                },
            }
            cells.append(rank_node)

            # Переменные для отслеживания максимальной высоты элементов ранга
            max_mission_branch_y = rank_y
            max_artifact_y = rank_y

            # Обрабатываем ветки миссий для этого ранга
            mission_branch_y = rank_y + config["mission_branch_height"]
            for mission_branch in rank.get("mission_branches", []):
                mission_branch_id = f"mission-branch-{mission_branch['id']}"
                default_mission_branch_x = 150 + (mission_branch["id"] - 1) * config["horizontal_spacing"]
                mission_branch_x, mission_branch_y = get_coordinates_from_data(
                    mission_branch_id, default_mission_branch_x, mission_branch_y
                )

                mission_branch_node = {
                    "id": mission_branch_id,
                    "shape": "mission-branch-node",
                    "x": mission_branch_x,
                    "y": mission_branch_y,
                    "attrs": {
                        "title": {"text": mission_branch["name"]},
                        "description": {"text": mission_branch["description"]},
                    },
                    "data": {
                        "type": "missionBranch",
                        "name": mission_branch["name"],
                        "description": mission_branch["description"],
                        "category": mission_branch["category"]["name"],
                        "time_to_complete": mission_branch["time_to_complete"],
                    },
                }
                cells.append(mission_branch_node)

                # Создаем связь от ранга к ветке миссий
                edge = {
                    "id": f"edge-{edge_counter}",
                    "shape": "entity-edge",
                    "source": {"cell": f"rank-{rank['id']}"},
                    "target": {"cell": f"mission-branch-{mission_branch['id']}"},
                }
                cells.append(edge)
                edge_counter += 1

                # Обрабатываем миссии в этой ветке
                mission_y = mission_branch_y + config["mission_height"]
                for mission in mission_branch.get("missions", []):
                    mission_id = f"mission-{mission['id']}"
                    default_mission_x = 100 + (mission["id"] - 1) * config["horizontal_spacing"]
                    mission_x, mission_y = get_coordinates_from_data(mission_id, default_mission_x, mission_y)

                    mission_node = {
                        "id": mission_id,
                        "shape": "mission-node",
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
                        "id": f"edge-{edge_counter}",
                        "shape": "entity-edge",
                        "source": {"cell": f"mission-branch-{mission_branch['id']}"},
                        "target": {"cell": f"mission-{mission['id']}"},
                    }
                    cells.append(edge)
                    edge_counter += 1

                    # Обрабатываем артефакты для этой миссии
                    artifact_y = mission_y + config["artifact_height"]
                    for artifact in mission.get("artifacts", []):
                        artifact_id = f"artifact-{artifact['id']}"
                        default_artifact_x = 100 + (artifact["id"] - 1) * config["horizontal_spacing"]
                        artifact_x, artifact_y = get_coordinates_from_data(artifact_id, default_artifact_x, artifact_y)

                        artifact_node = {
                            "id": artifact_id,
                            "shape": "artefact-node",
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
                            "id": f"edge-{edge_counter}",
                            "shape": "entity-edge",
                            "source": {"cell": f"mission-{mission['id']}"},
                            "target": {"cell": f"artifact-{artifact['id']}"},
                        }
                        cells.append(edge)
                        edge_counter += 1

                        # Обновляем максимальную высоту артефактов
                        max_artifact_y = max(max_artifact_y, artifact_y)
                        artifact_y += config["artifact_height"]

                    # Обновляем максимальную высоту миссий
                    max_mission_branch_y = max(max_mission_branch_y, mission_y)

                mission_branch_y += config["mission_branch_height"]

            # Рассчитываем позицию для событий на основе максимальной высоты элементов
            # Используем максимальную высоту из артефактов или веток миссий
            max_element_height = max(max_mission_branch_y, max_artifact_y)
            event_y = max_element_height + config["event_height"]

            # Обрабатываем события для этого ранга
            for event in rank.get("events", []):
                event_id = f"event-{event['id']}"
                event_x, event_y = get_coordinates_from_data(event_id, config["initial_x"], event_y)

                event_node = {
                    "id": event_id,
                    "shape": "event-node",
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

                # Создаем связи от всех артефактов к событию
                for mission_branch in rank.get("mission_branches", []):
                    for mission in mission_branch.get("missions", []):
                        for artifact in mission.get("artifacts", []):
                            edge = {
                                "id": f"edge-{edge_counter}",
                                "shape": "entity-edge",
                                "source": {"cell": f"artifact-{artifact['id']}"},
                                "target": {"cell": f"event-{event['id']}"},
                            }
                            cells.append(edge)
                            edge_counter += 1

                # Также создаем связь от ранга к событию
                edge = {
                    "id": f"edge-{edge_counter}",
                    "shape": "entity-edge",
                    "source": {"cell": f"rank-{rank['id']}"},
                    "target": {"cell": f"event-{event['id']}"},
                }
                cells.append(edge)
                edge_counter += 1

                event_y += config["event_height"]

            # Обновляем расстояние между рангами на основе фактической высоты текущего ранга
            if rank["id"] < len(game_world_data.get("ranks", [])):
                current_rank_height = event_y - rank_y
                config["rank_height"] = max(config["rank_height"], current_rank_height + 50)  # добавляем отступ

        return {"cells": cells}


game_world_service = GameWorldService()
