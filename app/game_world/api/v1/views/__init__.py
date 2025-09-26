from game_world.api.v1.views.activity_category import (
    ActivityCategoryCreateAPIView,
    ActivityCategoryDeleteAPIView,
    ActivityCategoryDetailAPIView,
    ActivityCategoryListAPIView,
    ActivityCategoryUpdateAPIView,
)
from game_world.api.v1.views.artifact import (
    ArtifactCreateAPIView,
    ArtifactDeleteAPIView,
    ArtifactListAPIView,
    ArtifactUpdateAPIView,
)
from game_world.api.v1.views.event import (
    EventCreateAPIView,
    EventDeleteAPIView,
    EventDetailAPIView,
    EventListAPIView,
    EventUpdateAPIView,
)
from game_world.api.v1.views.game_world import (
    GameWorldCreateAPIView,
    GameWorldDeleteAPIView,
    GameWorldDetailAPIView,
    GameWorldListAPIView,
    GameWorldRatingAPIView,
    GameWorldStatisticsAPIView,
    GameWorldUpdateAPIView,
)
from game_world.api.v1.views.mission import (
    MissionCreateAPIView,
    MissionDeleteAPIView,
    MissionDetailAPIView,
    MissionListAPIView,
    MissionUpdateAPIView,
)
from game_world.api.v1.views.mission_branch import (
    MissionBranchCreateAPIView,
    MissionBranchDeleteAPIView,
    MissionBranchDetailAPIView,
    MissionBranchListAPIView,
    MissionBranchUpdateAPIView,
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
    "GameWorldRatingAPIView",
    "GameWorldStatisticsAPIView",
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
    # ActivityCategory
    "ActivityCategoryListAPIView",
    "ActivityCategoryDetailAPIView",
    "ActivityCategoryCreateAPIView",
    "ActivityCategoryUpdateAPIView",
    "ActivityCategoryDeleteAPIView",
)
