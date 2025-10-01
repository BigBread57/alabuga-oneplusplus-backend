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

    def update_or_create_all_entities(
        self,
        game_world: int,
        cells_data: dict[str, Any],
    ):
        """
        Обновляет существующие сущности в БД или создает новые на основе данных графа
        """
        game_world_id = game_world.id
        game_world.data_for_graph = cells_data
        game_world.save()

        # Обрабатываем fk связи. Ключ - название связи, значения - словарь, где ключ и значение это uuid.
        relationship_fk_maps = defaultdict(dict)

        # Обрабатываем m2m связи. Ключ - название связи, значения - словарь, где ключ и значение это uuid.
        relationship_m2m_maps = defaultdict(lambda: defaultdict(list))

        for cell in cells_data.get("cells", []):
            cell_shape = cell["shape"]
            cell_data = cell["data"]

            # Создание или обновление Rank.
            if cell_shape == "rank":
                Rank.objects.update_or_create(
                    uuid=cell.get("uuid"), defaults={"game_world_id": game_world_id, **cell_data}
                )
            # Создание или обновление MissionBranch.
            if cell_shape == "mission_branch":
                MissionBranch.objects.update_or_create(
                    uuid=cell.get("uuid"), defaults={"game_world_id": game_world_id, **cell_data}
                )

            # Создание или обновление Mission.
            if cell_shape == "mission":
                Mission.objects.update_or_create(
                    uuid=cell.get("uuid"), defaults={"game_world_id": game_world_id, **cell_data}
                )

            # Создание или обновление Artifact.
            if cell_shape == "artifact":
                Artifact.objects.update_or_create(
                    uuid=cell.get("uuid"), defaults={"game_world_id": game_world_id, **cell_data}
                )

            # Создание или обновление Competency.
            if cell_shape == "competency":
                Competency.objects.update_or_create(
                    uuid=cell.get("uuid"), defaults={"game_world_id": game_world_id, **cell_data}
                )

            # Создание или обновление Competency.
            if cell_shape == "event":
                Event.objects.update_or_create(
                    uuid=cell.get("uuid"), defaults={"game_world_id": game_world_id, **cell_data}
                )

            # Создание или обновление Competency.
            if cell_shape == "game_world_story":
                GameWorldStory.objects.update_or_create(
                    uuid=cell.get("uuid"), defaults={"game_world_id": game_world_id, **cell_data}
                )

            # Формирование связей.
            if cell_shape == "edge":
                if cell_data["source_type"] == cell_data["target_type"]:
                    relationship_fk_maps[cell_data["source_type"]].update(
                        {cell["source"]["cell"]: cell["target"]["cell"]},
                    )
                elif cell_data["source_type"] == "mission" and cell_data["target_type"] == "artifact":
                    key = f"{cell_data['source_type']}|{cell['target_type']}"
                    relationship_m2m_maps[key][cell["source"]["cell"]].append(cell["target"]["cell"])
                else:
                    key = f"{cell_data['source_type']}|{cell['target_type']}"
                    relationship_fk_maps[key].update(
                        {cell["source"]["cell"]: cell["target"]["cell"]},
                    )

        # Установка связей.
        for relationship_name, relationships in relationship_fk_maps.items():
            # Ранг.
            if relationship_name == "rank":
                rank_for_update = []
                for rank in Rank.objects.filter(uuid__in=relationships.keys()):
                    rank.parent = relationships.get(rank.uuid)
                Rank.objects.bulk_update(rank_for_update, fields=("parent",))

            # Истории игрового мира и ранг.
            if relationship_name == "rank|game_world_story":
                game_world_stories_for_update = []
                game_world_stories_map = {
                    game_world_story.uuid: game_world_story
                    for game_world_story in GameWorldStory.objects.filter(uuid__in=relationships.values())
                }
                for rank in Rank.objects.filter(uuid__in=relationships.keys()):
                    game_world_story = game_world_stories_map.get(relationships.get(rank.uuid))
                    game_world_story.content_object = rank
                    game_world_stories_for_update.append(game_world_story)
                GameWorldStory.objects.bulk_update(game_world_stories_for_update, fields=("content_object",))

            # Истории игрового мира и артефакт.
            if relationship_name == "artifact|game_world_story":
                game_world_stories_for_update = []
                game_world_stories_map = {
                    game_world_story.uuid: game_world_story
                    for game_world_story in GameWorldStory.objects.filter(uuid__in=relationships.values())
                }
                for artifact in Artifact.objects.filter(uuid__in=relationships.keys()):
                    game_world_story = game_world_stories_map.get(relationships.get(artifact.uuid))
                    game_world_story.content_object = artifact
                    game_world_stories_for_update.append(game_world_story)
                GameWorldStory.objects.bulk_update(game_world_stories_for_update, fields=("content_object",))

            # Истории игрового мира и компетенция.
            if relationship_name == "artifact|game_world_story":
                game_world_stories_for_update = []
                game_world_stories_map = {
                    game_world_story.uuid: game_world_story
                    for game_world_story in GameWorldStory.objects.filter(uuid__in=relationships.values())
                }
                for competency in Competency.objects.filter(uuid__in=relationships.keys()):
                    game_world_story = game_world_stories_map.get(relationships.get(competency.uuid))
                    game_world_story.content_object = competency
                    game_world_stories_for_update.append(game_world_story)
                GameWorldStory.objects.bulk_update(game_world_stories_for_update, fields=("content_object",))

            # Ветка миссии и ранг.
            if relationship_name == "rank|mission_branch":
                mission_branches_for_update = []
                mission_branches_map = {
                    mission_branch.uuid: mission_branch
                    for mission_branch in MissionBranch.objects.filter(uuid__in=relationships.values())
                }
                for rank in Rank.objects.filter(uuid__in=relationships.keys()):
                    mission_branch = mission_branches_map.get(relationships.get(rank.uuid))
                    mission_branch.rank = rank
                    mission_branches_for_update.append(mission_branch)
                MissionBranch.objects.bulk_update(mission_branches_for_update, fields=("rank",))

            # Ветка миссии и миссия.
            if relationship_name == "mission_branch|mission":
                missions_for_update = []
                missions_map = {
                    mission.uuid: mission for mission in Mission.objects.filter(uuid__in=relationships.values())
                }
                for mission_branch in MissionBranch.objects.filter(uuid__in=relationships.keys()):
                    mission = missions_map.get(relationships.get(rank.uuid))
                    mission.branch = mission_branch
                Mission.objects.bulk_update(missions_for_update, fields=("mission_branch",))

        for relationship_name, relationships in relationship_m2m_maps.items():
            # Миссия и артефакт.
            if relationship_name == "mission|artifact":
                for mission_uuid, artifacts in relationships.items():
                    mission = Mission.objects.get(uuid=mission_uuid)
                    mission_artifact_for_create = [
                        MissionArtifact(
                            mission=mission,
                            artifact=artifact,
                        )
                        for artifact in Artifact.objects.filter(uuid__in=artifacts)
                    ]
                    MissionArtifact.objects.bulk_create(
                        mission_artifact_for_create,
                        ignore_conflicts=True,
                    )

        for relationship_name, relationships in relationship_m2m_maps.items():
            # Миссия и компетенция.
            if relationship_name == "mission|competency":
                for mission_uuid, competencies in relationships.items():
                    mission = Mission.objects.get(uuid=mission_uuid)
                    mission_artifact_for_create = [
                        MissionCompetency(
                            mission=mission,
                            competency=competency,
                            # TODO: Временное решение.
                            experience=50,
                        )
                        for competency in Competency.objects.filter(uuid__in=competencies)
                    ]
                    MissionCompetency.objects.bulk_create(
                        mission_artifact_for_create,
                        ignore_conflicts=True,
                    )

        for relationship_name, relationships in relationship_m2m_maps.items():
            # Событие и артефакт.
            if relationship_name == "event|artifact":
                for event_uuid, artifacts in relationships.items():
                    event = Mission.objects.get(uuid=event_uuid)
                    event_artifact_for_create = [
                        EventArtifact(
                            event=event,
                            artifact=artifact,
                        )
                        for artifact in Artifact.objects.filter(uuid__in=artifacts)
                    ]
                    EventArtifact.objects.bulk_create(
                        event_artifact_for_create,
                        ignore_conflicts=True,
                    )

        for relationship_name, relationships in relationship_m2m_maps.items():
            # Событие и компетенция.
            if relationship_name == "event|competency":
                for event_uuid, competencies in relationships.items():
                    event = Event.objects.get(uuid=event_uuid)
                    event_artifact_for_create = [
                        EventCompetency(
                            event=event,
                            competency=competency,
                            # TODO: Временное решение.
                            experience=50,
                        )
                        for competency in Competency.objects.filter(uuid__in=competencies)
                    ]
                    EventCompetency.objects.bulk_create(
                        event_artifact_for_create,
                        ignore_conflicts=True,
                    )

    def get_data_for_graph(self, game_world_data: dict[str, Any], data_for_graph: dict[str, Any] | None = None):
        """
        Преобразует объект игрового мира в формат cells для визуализации графа
        """
        cells = []
        all_uuid = []

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
            rank_uuid = rank["uuid"]
            default_rank_y = config["initial_y"] + (rank["id"] - 1) * config["rank_height"]
            rank_x, rank_y = get_coordinates_from_data(rank_uuid, config["initial_x"], default_rank_y)

            rank_node = {
                "id": rank_uuid,
                "shape": "rank",
                "position": {
                    "x": rank_x,
                    "y": rank_y,
                },
                "z_index": 1,
                "size": {
                    "width": 250,
                    "height": 80,
                },
                "attrs": {
                    "title": {"text": rank["name"]},
                    "description": {"text": rank.get("description", "")},
                },
                "data": {
                    "name": rank["name"],
                    "description": rank.get("description", ""),
                    "required_experience": rank["required_experience"],
                    "icon": rank.get("icon", None),
                    "color": rank.get("color", ""),
                },
            }
            cells.append(rank_node)
            if rank.get("parent"):
                edge = {
                    "id": f"{rank_uuid}|{rank['parent']['uuid']}",
                    "shape": "edge",
                    "source": {"cell": rank_uuid},
                    "target": {"cell": rank["parent"]["uuid"]},
                    "z_index": -1,
                    "data": {
                        "source_type": "rank",
                        "target_type": "rank",
                    },
                }
                cells.append(edge)

            for game_world_story in rank.get("game_world_story", []):
                game_world_story_uuid = game_world_story["uuid"]
                game_world_story_node = {
                    "id": game_world_story_uuid,
                    "shape": "game_world_story",
                    "position": {
                        "x": rank_x,
                        "y": rank_y,
                    },
                    "z_index": 1,
                    "size": {
                        "width": 250,
                        "height": 80,
                    },
                    "attrs": {
                        "title": {"text": game_world_story["text"]},
                    },
                    "data": {
                        "image": game_world_story.get("image", None),
                        "text": game_world_story["text"],
                    },
                }
                cells.append(game_world_story_node)
                game_world_story_uuid = game_world_story["uuid"]
                edge = {
                    "id": f"{rank_uuid}|{game_world_story_uuid}",
                    "shape": "edge",
                    "source": {"cell": rank_uuid},
                    "target": {"cell": game_world_story_uuid},
                    "z_index": -1,
                    "data": {
                        "source_type": "rank",
                        "target_type": "game_world_story",
                    },
                }
                cells.append(edge)

            # Переменные для отслеживания максимальной высоты элементов ранга
            max_mission_branch_y = rank_y
            max_artifact_y = rank_y
            max_competency_y = rank_y

            # Обрабатываем ветки миссий для этого ранга
            mission_branch_y = rank_y + config["mission_branch_height"]
            for mission_branch in rank.get("mission_branches", []):
                mission_branch_uuid = mission_branch["uuid"]
                default_mission_branch_x = 150 + (mission_branch["id"] - 1) * config["horizontal_spacing"]
                mission_branch_x, mission_branch_y = get_coordinates_from_data(
                    mission_branch_uuid,
                    default_mission_branch_x,
                    mission_branch_y,
                )

                mission_branch_node = {
                    "id": mission_branch_uuid,
                    "shape": "mission_branch",
                    "position": {
                        "x": mission_branch_x,
                        "y": mission_branch_y,
                    },
                    "z_index": 1,
                    "size": {
                        "width": 250,
                        "height": 80,
                    },
                    "attrs": {
                        "title": {"text": mission_branch.get("name")},
                        "description": {"text": mission_branch.get("description", "")},
                    },
                    "data": {
                        "name": mission_branch["name"],
                        "description": mission_branch.get("description", ""),
                        "icon": mission_branch.get("icon", None),
                        "color": mission_branch.get("color", ""),
                        "is_active": mission_branch["is_active"],
                        "start_datetime": mission_branch.get("start_datetime", None),
                        "time_to_complete": mission_branch.get("time_to_complete", None),
                        "category": mission_branch["category"],
                        "mentor": mission_branch.get("mentor", None),
                    },
                }
                cells.append(mission_branch_node)

                # Создаем связь от ранга к ветке миссий
                edge = {
                    "id": f"{rank_uuid}|{mission_branch_uuid}",
                    "shape": "edge",
                    "source": {"cell": rank_uuid},
                    "target": {"cell": mission_branch_uuid},
                    "z_index": -1,
                    "data": {
                        "source_type": "rank",
                        "target_type": "mission_branch",
                    },
                }
                cells.append(edge)

                # Обрабатываем миссии в этой ветке
                mission_y = mission_branch_y + config["mission_height"]
                for mission in mission_branch.get("missions", []):
                    mission_uuid = mission["uuid"]
                    default_mission_x = 100 + (mission["id"] - 1) * config["horizontal_spacing"]
                    mission_x, mission_y = get_coordinates_from_data(mission_uuid, default_mission_x, mission_y)

                    mission_node = {
                        "id": mission_uuid,
                        "shape": "mission",
                        "position": {
                            "x": mission_x,
                            "y": mission_y,
                        },
                        "z_index": 1,
                        "size": {
                            "width": 250,
                            "height": 80,
                        },
                        "attrs": {
                            "title": {"text": mission["name"]},
                            "description": {"text": mission["description"]},
                        },
                        "data": {
                            "name": mission["name"],
                            "description": mission["description"],
                            "experience": mission["experience"],
                            "currency": mission["currency"],
                            "icon": mission.get("icon", None),
                            "color": mission.get("color", ""),
                            "order": mission["order"],
                            "is_key_mission": mission["is_key_mission"],
                            "is_active": mission["is_active"],
                            "time_to_complete": mission.get("time_to_complete", None),
                            "qr_code": mission.get("qr_code", None),
                            "level": mission.get("level"),
                            "category": mission.get("category"),
                            "mentor": mission.get("mentor", None),
                        },
                    }
                    cells.append(mission_node)

                    # Истории игрового мира.
                    for game_world_story in mission.get("game_world_story", []):
                        game_world_story_uuid = game_world_story["uuid"]
                        game_world_story_node = {
                            "id": game_world_story_uuid,
                            "shape": "game_world_story",
                            "position": {
                                "x": mission_x,
                                "y": mission_y,
                            },
                            "z_index": 1,
                            "size": {
                                "width": 250,
                                "height": 80,
                            },
                            "attrs": {
                                "title": {"text": game_world_story["text"]},
                            },
                            "data": {
                                "image": game_world_story.get("image", None),
                                "text": game_world_story["text"],
                            },
                        }
                        cells.append(game_world_story_node)

                        edge = {
                            "id": f"{mission_uuid}|{game_world_story_uuid}",
                            "shape": "edge",
                            "source": {"cell": mission_uuid},
                            "target": {"cell": game_world_story_uuid},
                            "z_index": -1,
                            "data": {
                                "source_type": "mission",
                                "target_type": "game_world_story",
                            },
                        }
                        cells.append(edge)

                    # Создаем связь от ветки миссий к миссии
                    edge = {
                        "id": f"{mission_branch_uuid}|{mission_uuid}",
                        "shape": "edge",
                        "source": {"cell": mission_branch_uuid},
                        "target": {"cell": mission_uuid},
                        "z_index": -1,
                        "data": {
                            "source_type": "mission_branch",
                            "target_type": "mission",
                        },
                    }
                    cells.append(edge)

                    # Обрабатываем артефакты для этой миссии
                    artifact_y = mission_y + config["artifact_height"]
                    for artifact in mission.get("artifacts", []):
                        artifact_uuid = artifact["uuid"]
                        default_artifact_x = 100 + (artifact["id"] - 1) * config["horizontal_spacing"]
                        artifact_x, artifact_y = get_coordinates_from_data(
                            artifact_uuid, default_artifact_x, artifact_y
                        )

                        artifact_node = {
                            "id": artifact_uuid,
                            "shape": "artifact",
                            "position": {
                                "x": artifact_x,
                                "y": artifact_y,
                            },
                            "z_index": 1,
                            "size": {
                                "width": 250,
                                "height": 80,
                            },
                            "attrs": {
                                "title": {"text": artifact["name"]},
                                "description": {"text": artifact.get("description", "")},
                            },
                            "data": {
                                "name": artifact["name"],
                                "description": artifact.get("description", ""),
                                "icon": artifact.get("icon", None),
                                "color": artifact.get("color", ""),
                                "modifier": artifact["modifier"],
                                "modifier_value": artifact["modifier_value"],
                            },
                        }
                        cells.append(artifact_node)

                        # Истории игрового мира.
                        for game_world_story in artifact.get("game_world_story", []):
                            game_world_story_uuid = game_world_story["uuid"]
                            game_world_story_node = {
                                "id": game_world_story_uuid,
                                "shape": "game_world_story",
                                "position": {
                                    "x": artifact_x,
                                    "y": artifact_y,
                                },
                                "z_index": 1,
                                "size": {
                                    "width": 250,
                                    "height": 80,
                                },
                                "attrs": {
                                    "title": {"text": game_world_story["text"]},
                                },
                                "data": {
                                    "image": game_world_story.get("image", None),
                                    "text": game_world_story["text"],
                                },
                            }
                            cells.append(game_world_story_node)

                            edge = {
                                "id": f"{artifact_uuid}|{game_world_story_uuid}",
                                "shape": "edge",
                                "source": {"cell": artifact_uuid},
                                "target": {"cell": game_world_story_uuid},
                                "z_index": -1,
                                "data": {
                                    "source_type": "artifact",
                                    "target_type": "game_world_story",
                                },
                            }
                            cells.append(edge)

                        # Создаем связь от миссии к артефакту
                        edge = {
                            "id": f"{mission_uuid}|{artifact_uuid}",
                            "shape": "edge",
                            "source": {"cell": mission_uuid},
                            "target": {"cell": artifact_uuid},
                            "z_index": -1,
                            "data": {
                                "source_type": "mission",
                                "target_type": "artifact",
                            },
                        }
                        cells.append(edge)

                        # Обновляем максимальную высоту артефактов
                        max_artifact_y = max(max_artifact_y, artifact_y)
                        artifact_y += config["artifact_height"]

                    # Обрабатываем компетенции для этой миссии
                    competency_y = mission_y + config["competency_height"]
                    for competency in mission.get("competencies", []):
                        competency_uuid = competency["uuid"]
                        default_competency_x = 100 + (competency["id"] - 1) * config["horizontal_spacing"]
                        competency_x, competency_y = get_coordinates_from_data(
                            competency_uuid, default_competency_x, competency_y
                        )

                        competency_node = {
                            "id": competency_uuid,
                            "shape": "competency",
                            "position": {
                                "x": competency_x,
                                "y": competency_y,
                            },
                            "z_index": 1,
                            "size": {
                                "width": 250,
                                "height": 80,
                            },
                            "attrs": {
                                "title": {"text": competency["name"]},
                                "description": {"text": competency.get("description", "")},
                            },
                            "data": {
                                "name": competency["name"],
                                "description": competency.get("description", ""),
                                "required_experience": competency["required_experience"],
                                "level": competency["level"],
                                "icon": competency.get("icon", None),
                                "color": competency.get("color", ""),
                            },
                        }
                        cells.append(competency_node)

                        # Истории игрового мира.
                        for game_world_story in competency.get("game_world_story", []):
                            game_world_story_uuid = game_world_story["uuid"]
                            game_world_story_node = {
                                "id": game_world_story_uuid,
                                "shape": "game_world_story",
                                "position": {
                                    "x": competency_x,
                                    "y": competency_y,
                                },
                                "z_index": 1,
                                "size": {
                                    "width": 250,
                                    "height": 80,
                                },
                                "attrs": {
                                    "title": {"text": game_world_story["text"]},
                                },
                                "data": {
                                    "image": game_world_story.get("image", None),
                                    "text": game_world_story["text"],
                                },
                            }
                            cells.append(game_world_story_node)
                            edge = {
                                "id": f"{competency_uuid}|{game_world_story_uuid}",
                                "shape": "edge",
                                "source": {"cell": competency_uuid},
                                "target": {"cell": game_world_story_uuid},
                                "z_index": -1,
                                "data": {
                                    "source_type": "competency",
                                    "target_type": "game_world_story",
                                },
                            }
                            cells.append(edge)

                        if competency.get("parent"):
                            edge = {
                                "id": f"{competency_uuid}|{competency['parent']['uuid']}",
                                "shape": "edge",
                                "source": {"cell": competency_uuid},
                                "target": {"cell": competency["parent"]["uuid"]},
                                "z_index": -1,
                                "data": {
                                    "source_type": "competency",
                                    "target_type": "competency",
                                },
                            }
                            cells.append(edge)

                        # Создаем связь от миссии к компетенции
                        edge = {
                            "id": f"{mission_uuid}|{competency_uuid}",
                            "shape": "edge",
                            "source": {"cell": mission_uuid},
                            "target": {"cell": competency_uuid},
                            "z_index": -1,
                            "data": {
                                "source_type": "mission",
                                "target_type": "competency",
                            },
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
                event_uuid = event["uuid"]
                event_x, event_y = get_coordinates_from_data(event_uuid, config["initial_x"], event_y)

                event_node = {
                    "id": event_uuid,
                    "shape": "event",
                    "position": {
                        "x": event_x,
                        "y": event_y,
                    },
                    "z_index": 1,
                    "size": {
                        "width": 250,
                        "height": 80,
                    },
                    "attrs": {
                        "title": {"text": event.get("name")},
                        "description": {"text": event.get("description", "")},
                    },
                    "data": {
                        "type": "event",
                        "name": event["name"],
                        "description": event["description"],
                        "experience": event["experience"],
                        "currency": event["currency"],
                        "icon": event.get("icon", None),
                        "color": event.get("color", ""),
                        "required_number": event["required_number"],
                        "is_active": event["is_active"],
                        "start_datetime": event.get("start_datetime", None),
                        "time_to_complete": event.get("time_to_complete", None),
                        "qr_code": event.get("qr_code", None),
                        "category": event.get("category"),
                        "mentor": event.get("mentor", None),
                    },
                }
                cells.append(event_node)

                # Истории игрового мира.
                for game_world_story in event.get("game_world_story", []):
                    game_world_story_uuid = game_world_story["uuid"]
                    game_world_story_node = {
                        "id": game_world_story_uuid,
                        "shape": "game_world_story",
                        "position": {
                            "x": event_x,
                            "y": event_y,
                        },
                        "z_index": 1,
                        "size": {
                            "width": 250,
                            "height": 80,
                        },
                        "attrs": {
                            "title": {"text": game_world_story["text"]},
                        },
                        "data": {
                            "image": game_world_story.get("image", None),
                            "text": game_world_story["text"],
                        },
                    }
                    cells.append(game_world_story_node)
                    edge = {
                        "id": f"{event_uuid}|{game_world_story_uuid}",
                        "shape": "edge",
                        "source": {"cell": event_uuid},
                        "target": {"cell": game_world_story_uuid},
                        "z_index": -1,
                        "data": {
                            "source_type": "event",
                            "target_type": "game_world_story",
                        },
                    }
                    cells.append(edge)

                # Создаем связь от ранга к ветке миссий
                edge = {
                    "id": f"{rank_uuid}|{event_uuid}",
                    "shape": "edge",
                    "source": {"cell": rank_uuid},
                    "target": {"cell": event_uuid},
                    "z_index": -1,
                    "data": {
                        "source_type": "rank",
                        "target_type": "event",
                    },
                }
                cells.append(edge)

                # Обрабатываем артефакты для этой миссии
                artifact_y = event_y + config["artifact_height"]
                for artifact in event.get("artifacts", []):
                    artifact_uuid = artifact["uuid"]
                    default_artifact_x = 100 + (artifact["id"] - 1) * config["horizontal_spacing"]
                    artifact_x, artifact_y = get_coordinates_from_data(artifact_uuid, default_artifact_x, artifact_y)

                    artifact_node = {
                        "id": artifact_uuid,
                        "shape": "artifact",
                        "position": {
                            "x": artifact_x,
                            "y": artifact_y,
                        },
                        "z_index": 1,
                        "size": {
                            "width": 250,
                            "height": 80,
                        },
                        "attrs": {
                            "title": {"text": artifact["name"]},
                            "description": {"text": artifact.get("description", "")},
                        },
                        "data": {
                            "name": artifact["name"],
                            "description": artifact.get("description", ""),
                            "icon": artifact.get("icon", None),
                            "color": artifact.get("color", ""),
                            "modifier": artifact["modifier"],
                            "modifier_value": artifact["modifier_value"],
                        },
                    }
                    cells.append(artifact_node)

                    # Истории игрового мира.
                    for game_world_story in artifact.get("game_world_story", []):
                        game_world_story_uuid = game_world_story["uuid"]
                        game_world_story_node = {
                            "id": game_world_story_uuid,
                            "shape": "game_world_story",
                            "position": {
                                "x": artifact_x,
                                "y": artifact_y,
                            },
                            "z_index": 1,
                            "size": {
                                "width": 250,
                                "height": 80,
                            },
                            "attrs": {
                                "title": {"text": game_world_story["text"]},
                            },
                            "data": {
                                "image": game_world_story.get("image", None),
                                "text": game_world_story["text"],
                            },
                        }
                        cells.append(game_world_story_node)
                        edge = {
                            "id": f"{artifact_uuid}|{game_world_story_uuid}",
                            "shape": "edge",
                            "source": {"cell": artifact_uuid},
                            "target": {"cell": game_world_story_uuid},
                            "z_index": -1,
                            "data": {
                                "source_type": "artifact",
                                "target_type": "game_world_story",
                            },
                        }
                        cells.append(edge)

                    # Создаем связь от миссии к артефакту
                    edge = {
                        "id": f"{event_uuid}|{artifact_uuid}",
                        "shape": "edge",
                        "source": {"cell": event_uuid},
                        "target": {"cell": artifact_uuid},
                        "z_index": -1,
                        "data": {
                            "source_type": "event",
                            "target_type": "artifact",
                        },
                    }
                    cells.append(edge)

                    # Обновляем максимальную высоту артефактов
                    max_artifact_y = max(max_artifact_y, artifact_y)
                    artifact_y += config["artifact_height"]

                # Обрабатываем компетенции для этой миссии
                competency_y = event_y + config["competency_height"]
                for competency in event.get("competencies", []):
                    competency_uuid = competency["uuid"]
                    default_competency_x = 100 + (competency["id"] - 1) * config["horizontal_spacing"]
                    competency_x, competency_y = get_coordinates_from_data(
                        competency_uuid, default_competency_x, competency_y
                    )

                    competency_node = {
                        "id": competency_uuid,
                        "shape": "competency",
                        "position": {
                            "x": competency_x,
                            "y": competency_y,
                        },
                        "z_index": 1,
                        "size": {
                            "width": 250,
                            "height": 80,
                        },
                        "attrs": {
                            "title": {"text": competency["name"]},
                            "description": {"text": competency.get("description", "")},
                        },
                        "data": {
                            "name": competency["name"],
                            "description": competency.get("description", ""),
                            "required_experience": competency["required_experience"],
                            "level": competency["level"],
                            "icon": competency.get("icon", None),
                            "color": competency.get("color", ""),
                        },
                    }
                    cells.append(competency_node)

                    # Истории игрового мира.
                    for game_world_story in competency.get("game_world_story", []):
                        game_world_story_uuid = game_world_story["uuid"]
                        game_world_story_node = {
                            "id": game_world_story_uuid,
                            "shape": "game_world_story",
                            "x": competency_x,
                            "y": competency_y,
                            "attrs": {
                                "title": {"text": game_world_story["text"]},
                            },
                            "data": {
                                "image": game_world_story.get("image", None),
                                "text": game_world_story["text"],
                            },
                        }
                        cells.append(game_world_story_node)
                        edge = {
                            "id": f"{competency_uuid}|{game_world_story_uuid}",
                            "shape": "edge",
                            "source": {"cell": competency_uuid},
                            "target": {"cell": game_world_story_uuid},
                            "z_index": -1,
                            "data": {
                                "source_type": "competency",
                                "target_type": "game_world_story",
                            },
                        }
                        cells.append(edge)

                    if competency.get("parent"):
                        edge = {
                            "id": f"{competency_uuid}|{competency['parent']['uuid']}",
                            "shape": "edge",
                            "source": {"cell": competency_uuid},
                            "target": {"cell": competency["parent"]["uuid"]},
                            "z_index": -1,
                            "data": {
                                "source_type": "competency",
                                "target_type": "competency",
                            },
                        }
                        cells.append(edge)

                    # Создаем связь от миссии к компетенции
                    edge = {
                        "id": f"{event_uuid}|{competency_uuid}",
                        "shape": "edge",
                        "source": {"cell": event_uuid},
                        "target": {"cell": competency_uuid},
                        "z_index": -1,
                        "data": {
                            "source_type": "event",
                            "target_type": "competency",
                        },
                    }
                    cells.append(edge)

                    # Обновляем максимальную высоту компетенций
                    max_competency_y = max(max_competency_y, competency_y)
                    competency_y += config["competency_height"]

                event_y += config["event_height"]

            # Обновляем расстояние между рангами на основе фактической высоты текущего ранга
            if rank["id"] < len(game_world_data.get("ranks", [])):
                current_rank_height = event_y - rank_y
                config["rank_height"] = max(config["rank_height"], current_rank_height + 50)  # добавляем отступ

        return {"cells": cells}


game_world_service = GameWorldService()
