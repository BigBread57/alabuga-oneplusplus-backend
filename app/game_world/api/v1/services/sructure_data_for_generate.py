from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class TargetMarker(BaseModel):
    fill: str


class Line(BaseModel):
    stroke: str
    targetMarker: TargetMarker


class AttrsEdge(BaseModel):
    line: Line


class AttrsNode(BaseModel):
    title: Dict[str, str]
    description: Dict[str, str]


class SourceTarget(BaseModel):
    cell: str


class DataEdge(BaseModel):
    source_type: str
    target_type: str


class DataCompetency(BaseModel):
    icon: Optional[str] = None
    name: str
    color: str
    level: int
    description: str
    required_experience: int


class DataRank(BaseModel):
    icon: Optional[str] = None
    name: str
    color: str
    description: str
    required_experience: int


class DataMissionBranch(BaseModel):
    icon: Optional[str] = None
    name: str
    color: str
    is_active: bool
    mentor_id: Optional[str] = None
    category_id: int
    description: str
    start_datetime: Optional[str] = None
    time_to_complete: int


class DataMission(BaseModel):
    icon: Optional[str] = None
    name: str
    color: str
    order: int
    qr_code: Optional[str] = None
    currency: int
    level_id: int
    is_active: bool
    mentor_id: Optional[str] = None
    experience: int
    category_id: int
    description: str
    is_key_mission: bool
    time_to_complete: int


class DataArtifact(BaseModel):
    icon: Optional[str] = None
    name: str
    color: str
    modifier: str
    description: str
    modifier_value: int


class DataEvent(BaseModel):
    icon: Optional[str] = None
    name: str
    type: str
    color: str
    qr_code: Optional[str] = None
    currency: int
    is_active: bool
    mentor_id: Optional[str] = None
    experience: int
    category_id: int
    description: str
    start_datetime: str
    required_number: int
    time_to_complete: int


class DataGameWorldStory(BaseModel):
    image: Optional[str] = None
    text: str


class Size(BaseModel):
    width: int
    height: int


class Position(BaseModel):
    x: int
    y: int


class Cell(BaseModel):
    id: str
    data: Dict[str, Any]
    attrs: Dict[str, Any]
    shape: str
    zIndex: int
    z_index: int
    source: Optional[SourceTarget] = None
    target: Optional[SourceTarget] = None
    size: Optional[Size] = None
    position: Optional[Position] = None


class CellStructure(BaseModel):
    cells: List[Cell]


# Альтернативная версия с более строгой типизацией для разных типов ячеек
class BaseCellData(BaseModel):
    icon: Optional[str] = None
    name: str
    color: str
    description: str


class CompetencyData(BaseCellData):
    level: int
    required_experience: int


class RankData(BaseCellData):
    required_experience: int


class MissionBranchData(BaseCellData):
    is_active: bool
    mentor_id: Optional[str] = None
    category_id: int
    start_datetime: Optional[str] = None
    time_to_complete: int


class MissionData(BaseCellData):
    order: int
    qr_code: Optional[str] = None
    currency: int
    level_id: int
    is_active: bool
    mentor_id: Optional[str] = None
    experience: int
    category_id: int
    is_key_mission: bool
    time_to_complete: int


class ArtifactData(BaseCellData):
    modifier: str
    modifier_value: int


class EventData(BaseCellData):
    type: str
    qr_code: Optional[str] = None
    currency: int
    is_active: bool
    mentor_id: Optional[str] = None
    experience: int
    category_id: int
    start_datetime: str
    required_number: int
    time_to_complete: int


# Модель для удобной работы с разными типами ячеек
class TypedCellStructure(BaseModel):
    cells: List[Cell]

    def get_cells_by_shape(self, shape: str) -> List[Cell]:
        return [cell for cell in self.cells if cell.shape == shape]

    def get_edges(self) -> List[Cell]:
        return self.get_cells_by_shape("edge")

    def get_nodes(self) -> List[Cell]:
        return [cell for cell in self.cells if cell.shape != "edge"]

    def get_competencies(self) -> List[Cell]:
        return self.get_cells_by_shape("competency")

    def get_ranks(self) -> List[Cell]:
        return self.get_cells_by_shape("rank")

    def get_mission_branches(self) -> List[Cell]:
        return self.get_cells_by_shape("mission_branch")

    def get_missions(self) -> List[Cell]:
        return self.get_cells_by_shape("mission")

    def get_artifacts(self) -> List[Cell]:
        return self.get_cells_by_shape("artifact")

    def get_events(self) -> List[Cell]:
        return self.get_cells_by_shape("event")

    def get_game_world_stories(self) -> List[Cell]:
        return self.get_cells_by_shape("game_world_story")