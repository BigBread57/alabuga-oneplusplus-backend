from app.game_world.api.v1.views.artifact import (
    ArtifactListAPIView,
    ArtifactCreateAPIView,
    ArtifactUpdateAPIView,
    ArtifactDeleteAPIView,
)
from app.game_world.api.v1.views.event import (
    EventListAPIView,
    EventCreateAPIView,
    EventUpdateAPIView,
    EventDeleteAPIView,
    EventDetailAPIView,
)
from app.game_world.api.v1.views.game_world import (
    GameWorldListAPIView,
    GameWorldDetailAPIView,
    GameWorldUpdateAPIView,
    GameWorldCreateAPIView,
    GameWorldDeleteAPIView,
)
from app.game_world.api.v1.views.mission import (
    MissionListAPIView,
    MissionDetailAPIView,
    MissionCreateAPIView,
    MissionUpdateAPIView,
    MissionDeleteAPIView,
)
from app.game_world.api.v1.views.mission_branch import (
    MissionBranchListAPIView,
    MissionBranchDeleteAPIView,
    MissionBranchUpdateAPIView,
    MissionBranchDetailAPIView,
    MissionBranchCreateAPIView,
)
from app.game_world.api.v1.views.mission_category import (
    MissionCategoryListAPIView,
    MissionCategoryDetailAPIView,
    MissionCategoryUpdateAPIView,
    MissionCategoryCreateAPIView,
    MissionCategoryDeleteAPIView,
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
