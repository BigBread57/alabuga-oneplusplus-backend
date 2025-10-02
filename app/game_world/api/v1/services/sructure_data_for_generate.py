from datetime import datetime
from uuid import UUID

from django.utils.translation import gettext as _
from pydantic import BaseModel, Field


class CompetencyBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название компетенции в рамках игрового мира"),
    )
    description: str = Field(
        ...,
        description=_("Описание компетенции в рамках игрового мира"),
    )
    required_experience: int = Field(
        ...,
        description=_(
            "Количество опыта, которое необходимо получить чтобы полностью "
            "изучить компетенцию и получить новую компетенцию"
        ),
    )
    parent_uuid: UUID | None = Field(
        None,
        description=_("UUID родительской компетенции"),
    )
    game_world_uuid: UUID = Field(
        ...,
        description=_("UUID игрового мира"),
    )


class RankBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название ранга в рамках игрового мира"),
    )
    description: str = Field(
        ...,
        description=_("Описание ранга в рамках игрового мира"),
    )
    required_experience: int = Field(
        ...,
        description=_(
            "Количество опыта, которое необходимо получить чтобы полностью закрыть ранг и получить новый ранг"
        ),
    )
    parent_uuid: UUID | None = Field(
        None,
        description=_("UUID родительского ранга"),
    )
    game_world_uuid: UUID = Field(
        ...,
        description=_("UUID игрового мира"),
    )


class RequiredRankCompetencyBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    rank_uuid: UUID = Field(
        ...,
        description=_("UUID ранга"),
    )
    competency_uuid: UUID = Field(
        ...,
        description=_("UUID компетенции"),
    )


class ActivityCategoryBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название категории активности"),
    )
    description: str = Field(
        ...,
        description=_("Описание категории активности"),
    )
    repeatability: int | None = Field(
        ...,
        description=_("Количество дней, через которую данную категории активности стоит повторить"),
    )


class ArtifactBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название артефакта"),
    )
    description: str = Field(
        ...,
        description=_("Описание артефакта"),
    )
    modifier: str | None = Field(
        None,
        description=_("Значение модификатора для артефакта"),
    )
    modifier_value: float | None = Field(
        None,
        description=_("Значение модификатора в %"),
    )
    game_world_uuid: UUID = Field(
        ...,
        description=_("UUID игрового мира"),
    )


class EventBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название события"),
    )
    description: str = Field(
        ...,
        description=_("Описание события"),
    )
    experience: int = Field(
        ...,
        description=_("Награда в опыте"),
    )
    currency: int = Field(
        ...,
        description=_("Награда в валюте"),
    )
    required_number: int = Field(
        ...,
        description=_("Количество персонажей для успеха"),
    )
    is_active: bool = Field(
        ...,
        description=_("Активно событие или нет"),
    )
    start_datetime: datetime | None = Field(
        None,
        description=_("Дата и время запуска"),
    )
    time_to_complete: int = Field(
        ...,
        description=_("Количество дней на выполнение"),
    )
    category_uuid: UUID = Field(
        ...,
        description=_("UUID категории"),
    )
    rank_uuid: UUID = Field(
        ...,
        description=_("UUID ранга"),
    )
    mentor_uuid: UUID | None = Field(
        None,
        description=_("UUID ментора"),
    )
    game_world_uuid: UUID = Field(
        ...,
        description=_("UUID игрового мира"),
    )


class EventArtifactBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    event_uuid: UUID = Field(
        ...,
        description=_("UUID события"),
    )
    artifact_uuid: UUID = Field(
        ...,
        description=_("UUID артефакта"),
    )


class EventCompetencyBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    experience: int = Field(
        ...,
        description=_("Опыт за компетенцию"),
    )
    event_uuid: UUID = Field(
        ...,
        description=_("UUID события"),
    )
    competency_uuid: UUID = Field(
        ...,
        description=_("UUID компетенции"),
    )


class GameWorldStoryBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    text: str = Field(
        ...,
        description=_("Описание истории, лора"),
    )
    game_world_uuid: UUID = Field(
        ...,
        description=_("UUID игрового мира"),
    )
    content_type: str = Field(
        ...,
        description=_("Тип содержимого"),
    )
    object_uuid: UUID = Field(
        ...,
        description=_("UUID объекта"),
    )


class MissionBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название миссии"),
    )
    description: str = Field(
        ...,
        description=_("Описание миссии"),
    )
    experience: int = Field(
        ...,
        description=_("Награда в опыте"),
    )
    currency: int = Field(
        ...,
        description=_("Награда в валюте"),
    )
    order: int = Field(
        ...,
        description=_("Порядок в ветке"),
    )
    is_key_mission: bool = Field(
        ...,
        description=_("Является ли миссия обязательной"),
    )
    is_active: bool = Field(
        ...,
        description=_("Активная миссия или нет"),
    )
    time_to_complete: int = Field(
        ...,
        description=_("Количество дней на выполнение"),
    )
    branch_uuid: UUID = Field(
        ...,
        description=_("UUID ветки миссии"),
    )
    category_uuid: UUID = Field(
        ...,
        description=_("UUID категории"),
    )
    mentor_uuid: UUID | None = Field(
        None,
        description=_("UUID ментора"),
    )
    game_world_uuid: UUID = Field(
        ...,
        description=_("UUID игрового мира"),
    )


class MissionArtifactBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    mission_uuid: UUID = Field(
        ...,
        description=_("UUID миссии"),
    )
    artifact_uuid: UUID = Field(
        ...,
        description=_("UUID артефакта"),
    )


class MissionBranchBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название ветки миссий"),
    )
    description: str = Field(
        ...,
        description=_("Описание ветки миссий"),
    )
    is_active: bool = Field(
        ...,
        description=_("Активная ветка или нет"),
    )
    start_datetime: datetime | None = Field(
        None,
        description=_("Дата и время запуска"),
    )
    time_to_complete: int = Field(
        ...,
        description=_("Количество дней на выполнение"),
    )
    rank_uuid: UUID = Field(
        ...,
        description=_("UUID ранга"),
    )
    category_uuid: UUID = Field(
        ...,
        description=_("UUID категории"),
    )
    mentor_uuid: UUID | None = Field(
        None,
        description=_("UUID ментора"),
    )
    game_world_uuid: UUID = Field(
        ...,
        description=_("UUID игрового мира"),
    )


class MissionCompetencyBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    experience: int = Field(
        ...,
        description=_("Опыт за компетенцию"),
    )
    mission_uuid: UUID = Field(
        ...,
        description=_("UUID миссии"),
    )
    competency_uuid: UUID = Field(
        ...,
        description=_("UUID компетенции"),
    )


class MissionLevelBase(BaseModel):
    uuid: UUID = Field(
        ...,
        description=_("UUID"),
    )
    name: str = Field(
        ...,
        description=_("Название уровня миссии"),
    )
    description: str = Field(
        ...,
        description=_("Описание уровня миссии"),
    )
    multiplier_experience: float = Field(
        ...,
        description=_("Множитель опыта в %"),
    )
    multiplier_currency: float = Field(
        ...,
        description=_("Множитель валюты в %"),
    )


class GameWorldDataModel(BaseModel):
    competencies: list[CompetencyBase] = Field(
        default_factory=list,
        description=_("Список компетенций"),
    )
    ranks: list[RankBase] = Field(
        default_factory=list,
        description=_("Список рангов"),
    )
    required_rank_competencies: list[RequiredRankCompetencyBase] = Field(
        default_factory=list,
        description=_("Требования к компетенциям для рангов"),
    )
    activity_categories: list[ActivityCategoryBase] = Field(
        default_factory=list,
        description=_("Категории активностей"),
    )
    artifacts: list[ArtifactBase] = Field(
        default_factory=list,
        description=_("Список артефактов"),
    )
    events: list[EventBase] = Field(
        default_factory=list,
        description=_("Список событий"),
    )
    event_artifacts: list[EventArtifactBase] = Field(
        default_factory=list,
        description=_("Артефакты за события"),
    )
    event_competencies: list[EventCompetencyBase] = Field(
        default_factory=list,
        description=_("Компетенции за события"),
    )
    game_world_stories: list[GameWorldStoryBase] = Field(
        default_factory=list,
        description=_("Истории игрового мира"),
    )
    missions: list[MissionBase] = Field(
        default_factory=list,
        description=_("Список миссий"),
    )
    mission_artifacts: list[MissionArtifactBase] = Field(
        default_factory=list,
        description=_("Артефакты за миссии"),
    )
    mission_branches: list[MissionBranchBase] = Field(
        default_factory=list,
        description=_("Ветки миссий"),
    )
    mission_competencies: list[MissionCompetencyBase] = Field(
        default_factory=list,
        description=_("Компетенции за миссии"),
    )
    mission_levels: list[MissionLevelBase] = Field(
        default_factory=list,
        description=_("Уровни сложности миссий"),
    )
