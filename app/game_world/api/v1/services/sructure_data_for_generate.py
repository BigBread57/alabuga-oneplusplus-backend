from uuid import uuid4

from pydantic import BaseModel, Field

# === БАЗОВЫЕ КОМПОНЕНТЫ ===


class TargetMarker(BaseModel):
    fill: str


class Line(BaseModel):
    stroke: str
    targetMarker: TargetMarker


class AttrsEdge(BaseModel):
    line: Line


class AttrsTitle(BaseModel):
    text: str


class AttrsDescription(BaseModel):
    text: str


class AttrsNode(BaseModel):
    title: AttrsTitle
    description: AttrsDescription


class SourceTarget(BaseModel):
    cell: str


class Position(BaseModel):
    x: int
    y: int


class Size(BaseModel):
    width: int = 250
    height: int = 80


# === DATA МОДЕЛИ ===


class DataEdge(BaseModel):
    source_type: str
    target_type: str


class DataCompetency(BaseModel):
    icon: str | None = None
    name: str
    color: str
    level: int
    description: str
    required_experience: int


class DataRank(BaseModel):
    icon: str | None = None
    name: str
    color: str
    description: str
    required_experience: int


class DataMissionBranch(BaseModel):
    icon: str | None = None
    name: str
    color: str
    is_active: bool
    mentor_id: str | None = None
    category_id: int
    description: str
    start_datetime: str | None = None
    time_to_complete: int


class DataMission(BaseModel):
    icon: str | None = None
    name: str
    color: str
    order: int
    qr_code: str | None = None
    currency: int
    level_id: int
    is_active: bool
    mentor_id: str | None = None
    experience: int
    category_id: int
    description: str
    is_key_mission: bool
    time_to_complete: int


class DataArtifact(BaseModel):
    icon: str | None = None
    name: str
    color: str
    modifier: str
    description: str
    modifier_value: int


class DataEvent(BaseModel):
    icon: str | None = None
    name: str
    type: str
    color: str
    qr_code: str | None = None
    currency: int
    is_active: bool
    mentor_id: str | None = None
    experience: int
    category_id: int
    description: str
    start_datetime: str
    required_number: int
    time_to_complete: int


class DataGameWorldStory(BaseModel):
    image: str | None = None
    text: str


# === ЯЧЕЙКИ ===


class Cell(BaseModel):
    id: str
    shape: str
    zIndex: int
    z_index: int


class EdgeCell(Cell):
    data: DataEdge
    attrs: AttrsEdge
    source: SourceTarget
    target: SourceTarget
    shape: str = "edge"
    zIndex: int = -1
    z_index: int = -1


class NodeCell(Cell):
    attrs: AttrsNode
    position: Position
    size: Size
    zIndex: int = 2
    z_index: int = 1


class CompetencyCell(NodeCell):
    data: DataCompetency
    shape: str = "competency"


class RankCell(NodeCell):
    data: DataRank
    shape: str = "rank"


class MissionBranchCell(NodeCell):
    data: DataMissionBranch
    shape: str = "mission_branch"


class MissionCell(NodeCell):
    data: DataMission
    shape: str = "mission"


class ArtifactCell(NodeCell):
    data: DataArtifact
    shape: str = "artifact"


class EventCell(NodeCell):
    data: DataEvent
    shape: str = "event"


class GameWorldStoryCell(NodeCell):
    data: DataGameWorldStory
    shape: str = "game_world_story"


# === СТРУКТУРА ДЛЯ LLM ===


class ConnectionSchema(BaseModel):
    """Связь между элементами"""

    from_type: str = Field(description="Тип источника: mission, rank, competency, mission_branch, artifact, event")
    from_index: int = Field(description="Индекс элемента в соответствующем массиве")
    to_type: str = Field(description="Тип цели: mission, rank, competency, mission_branch, artifact, event")
    to_index: int = Field(description="Индекс элемента в соответствующем массиве")
    color: str = Field(default="#283a97", description="Цвет связи в HEX")


class TypedCellStructure(BaseModel):
    """
    Структура игрового мира для генерации LLM.

    ИНСТРУКЦИИ ДЛЯ LLM:

    1. КОМПЕТЕНЦИИ (5-12 штук):
       - Основные навыки для развития персонажа
       - level: от 1 до 10
       - required_experience растет (100, 250, 500, 1000...)

    2. РАНГИ (4-7 штук):
       - Система прогрессии: Новичок -> Специалист -> Эксперт -> Мастер
       - required_experience: 0, 500, 2000, 5000, 10000...

    3. ВЕТКИ МИССИЙ (3-7 штук):
       - Разные направления деятельности
       - time_to_complete: 30-90 дней
       - category_id: уникальные значения от 1

    4. МИССИИ (5-15 на каждую ветку):
       - order: последовательность от 1
       - experience: 50-500
       - currency: 50-1000
       - is_key_mission: 2-3 ключевые миссии на ветку
       - time_to_complete: 3-30 дней

    5. АРТЕФАКТЫ (10-20 штук):
       - modifier: DEFAULT, EXPERIENCE_GAIN, CURRENCY_GAIN, SHOP_DISCOUNT
       - modifier_value: 0 для DEFAULT, 1-5 для остальных

    6. СОБЫТИЯ (3-10 штук, опционально):
       - type: workshop, competition, training, hackathon
       - start_datetime: формат ISO 8601 (2025-10-15T14:00:00)

    7. СВЯЗИ (connections):
       - Миссия->Миссия (последовательность): {'from_type': 'mission', 'from_index': 0, 'to_type': 'mission', 'to_index': 1}
       - Миссия->Артефакт (награда): {'from_type': 'mission', 'from_index': 5, 'to_type': 'artifact', 'to_index': 2}
       - Миссия->Компетенция (развитие): {'from_type': 'mission', 'from_index': 3, 'to_type': 'competency', 'to_index': 1}
       - Ранг->МиссияВетка (доступность): {'from_type': 'rank', 'from_index': 1, 'to_type': 'mission_branch', 'to_index': 0}
    """

    competencies: list[DataCompetency] = Field(default_factory=list)
    ranks: list[DataRank] = Field(default_factory=list)
    mission_branches: list[DataMissionBranch] = Field(default_factory=list)
    missions: list[DataMission] = Field(default_factory=list)
    artifacts: list[DataArtifact] = Field(default_factory=list)
    events: list[DataEvent] = Field(default_factory=list)
    game_world_stories: list[DataGameWorldStory] = Field(default_factory=list)
    connections: list[ConnectionSchema] = Field(default_factory=list)

    def to_cells(self) -> dict:
        """Конвертация в формат graph-редактора с правильными ID"""
        cells = []
        node_map: dict[tuple[str, int], str] = {}

        # Настройки расположения
        START_X, START_Y = 100, 100
        SPACING_X, SPACING_Y = 350, 150

        # Компетенции
        for idx, data in enumerate(self.competencies):
            node_id = str(uuid4())
            cells.append(
                {
                    "id": node_id,
                    "data": data.model_dump(),
                    "attrs": {"title": {"text": data.name}, "description": {"text": data.description}},
                    "shape": "competency",
                    "position": {"x": START_X + (idx % 4) * SPACING_X, "y": START_Y + (idx // 4) * SPACING_Y},
                    "size": {"width": 250, "height": 80},
                    "zIndex": 2,
                    "z_index": 1,
                }
            )
            node_map[("competency", idx)] = node_id

        # Ранги
        for idx, data in enumerate(self.ranks):
            node_id = str(uuid4())
            cells.append(
                {
                    "id": node_id,
                    "data": data.model_dump(),
                    "attrs": {"title": {"text": data.name}, "description": {"text": data.description}},
                    "shape": "rank",
                    "position": {"x": START_X + idx * SPACING_X, "y": START_Y + 500},
                    "size": {"width": 250, "height": 80},
                    "zIndex": 2,
                    "z_index": 1,
                }
            )
            node_map[("rank", idx)] = node_id

        # Ветки миссий
        for idx, data in enumerate(self.mission_branches):
            node_id = str(uuid4())
            cells.append(
                {
                    "id": node_id,
                    "data": data.model_dump(),
                    "attrs": {"title": {"text": data.name}, "description": {"text": data.description}},
                    "shape": "mission_branch",
                    "position": {"x": START_X + (idx % 3) * SPACING_X, "y": START_Y + 800},
                    "size": {"width": 300, "height": 100},
                    "zIndex": 2,
                    "z_index": 1,
                }
            )
            node_map[("mission_branch", idx)] = node_id

        # Миссии
        for idx, data in enumerate(self.missions):
            node_id = str(uuid4())
            cells.append(
                {
                    "id": node_id,
                    "data": data.model_dump(),
                    "attrs": {"title": {"text": data.name}, "description": {"text": data.description}},
                    "shape": "mission",
                    "position": {"x": START_X + (idx % 5) * SPACING_X, "y": START_Y + 1100 + (idx // 5) * SPACING_Y},
                    "size": {"width": 280, "height": 90},
                    "zIndex": 2,
                    "z_index": 1,
                }
            )
            node_map[("mission", idx)] = node_id

        # Артефакты
        for idx, data in enumerate(self.artifacts):
            node_id = str(uuid4())
            cells.append(
                {
                    "id": node_id,
                    "data": data.model_dump(),
                    "attrs": {"title": {"text": data.name}, "description": {"text": data.description}},
                    "shape": "artifact",
                    "position": {"x": START_X + (idx % 6) * SPACING_X, "y": START_Y + 1600},
                    "size": {"width": 230, "height": 80},
                    "zIndex": 2,
                    "z_index": 1,
                }
            )
            node_map[("artifact", idx)] = node_id

        # События
        for idx, data in enumerate(self.events):
            node_id = str(uuid4())
            cells.append(
                {
                    "id": node_id,
                    "data": data.model_dump(),
                    "attrs": {"title": {"text": data.name}, "description": {"text": data.description}},
                    "shape": "event",
                    "position": {"x": START_X + (idx % 4) * SPACING_X, "y": START_Y + 1900},
                    "size": {"width": 270, "height": 90},
                    "zIndex": 2,
                    "z_index": 1,
                }
            )
            node_map[("event", idx)] = node_id

        # Истории
        for idx, data in enumerate(self.game_world_stories):
            node_id = str(uuid4())
            cells.append(
                {
                    "id": node_id,
                    "data": data.model_dump(),
                    "attrs": {"title": {"text": "История игрового мира"}, "description": {"text": data.text[:100]}},
                    "shape": "game_world_story",
                    "position": {"x": START_X + (idx % 3) * SPACING_X, "y": START_Y + 2200},
                    "size": {"width": 300, "height": 100},
                    "zIndex": 2,
                    "z_index": 1,
                }
            )
            node_map[("game_world_story", idx)] = node_id

        # Связи (edges)
        for conn in self.connections:
            from_key = (conn.from_type, conn.from_index)
            to_key = (conn.to_type, conn.to_index)

            if from_key in node_map and to_key in node_map:
                source_id = node_map[from_key]
                target_id = node_map[to_key]
                edge_id = f"{source_id}|{target_id}"

                cells.append(
                    {
                        "id": edge_id,
                        "data": {"source_type": conn.from_type, "target_type": conn.to_type},
                        "attrs": {"line": {"stroke": conn.color, "targetMarker": {"fill": conn.color}}},
                        "shape": "edge",
                        "source": {"cell": source_id},
                        "target": {"cell": target_id},
                        "zIndex": -1,
                        "z_index": -1,
                    }
                )

        return {"cells": cells}
