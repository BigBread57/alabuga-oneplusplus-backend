from app.game_world.api.v1.views.artifact import (
    ArtifactCreateAPIView,
    ArtifactDeleteAPIView,
    ArtifactListAPIView,
    ArtifactUpdateAPIView,
)
from app.game_world.api.v1.views.event import (
    EventCreateAPIView,
    EventDeleteAPIView,
    EventDetailAPIView,
    EventListAPIView,
    EventUpdateAPIView,
)
from app.game_world.api.v1.views.game_world import (
    GameWorldCreateAPIView,
    GameWorldDeleteAPIView,
    GameWorldDetailAPIView,
    GameWorldListAPIView,
    GameWorldUpdateAPIView,
)
from app.game_world.api.v1.views.mission import (
    MissionCreateAPIView,
    MissionDeleteAPIView,
    MissionDetailAPIView,
    MissionListAPIView,
    MissionUpdateAPIView,
)
from app.game_world.api.v1.views.mission_branch import (
    MissionBranchCreateAPIView,
    MissionBranchDeleteAPIView,
    MissionBranchDetailAPIView,
    MissionBranchListAPIView,
    MissionBranchUpdateAPIView,
)
from app.game_world.api.v1.views.mission_category import (
    MissionCategoryCreateAPIView,
    MissionCategoryDeleteAPIView,
    MissionCategoryDetailAPIView,
    MissionCategoryListAPIView,
    MissionCategoryUpdateAPIView,
)

__all__ = (
    # Artifact
    "ArtifactListAPIView",
    "ArtifactCreateAPIView",
    "ArtifactUpdateAPIView",
    "ArtifactDeleteAPIView",
    # Event
    "EventListAPIView",
    "EventDetailAPIView",
    "EventCreateAPIView",
    "EventUpdateAPIView",
    "EventDeleteAPIView",
    # GameWorld
    "GameWorldListAPIView",
    "GameWorldDetailAPIView",
    "GameWorldCreateAPIView",
    "GameWorldUpdateAPIView",
    "GameWorldDeleteAPIView",
    # Mission
    "MissionListAPIView",
    "MissionDetailAPIView",
    "MissionCreateAPIView",
    "MissionUpdateAPIView",
    "MissionDeleteAPIView",
    # MissionBranch
    "MissionBranchListAPIView",
    "MissionBranchDetailAPIView",
    "MissionBranchCreateAPIView",
    "MissionBranchUpdateAPIView",
    "MissionBranchDeleteAPIView",
    # MissionCategory
    "MissionCategoryListAPIView",
    "MissionCategoryDetailAPIView",
    "MissionCategoryCreateAPIView",
    "MissionCategoryUpdateAPIView",
    "MissionCategoryDeleteAPIView",
)
