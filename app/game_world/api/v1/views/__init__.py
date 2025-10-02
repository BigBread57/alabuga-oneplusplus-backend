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
    EventCheckQrCodeAPIView,
    EventCreateAPIView,
    EventDeleteAPIView,
    EventDetailAPIView,
    EventListAPIView,
    EventUpdateAPIView,
)
from game_world.api.v1.views.event_artifact import (
    EventArtifactCreateAPIView,
    EventArtifactDeleteAPIView,
    EventArtifactDetailAPIView,
    EventArtifactListAPIView,
    EventArtifactUpdateAPIView,
)
from game_world.api.v1.views.event_competency import (
    EventCompetencyCreateAPIView,
    EventCompetencyDeleteAPIView,
    EventCompetencyDetailAPIView,
    EventCompetencyListAPIView,
    EventCompetencyUpdateAPIView,
)
from game_world.api.v1.views.game_world import (
    GameWorldCreateAPIView,
    GameWorldDataForGraphAPIView,
    GameWorldDeleteAPIView,
    GameWorldDetailAPIView,
    GameWorldGenerateAPIView,
    GameWorldInfoForGenerateAPIView,
    GameWorldListAPIView,
    GameWorldStatisticsAPIView,
    GameWorldUpdateAPIView,
    GameWorldUpdateOrCreateAllEntitiesAPIView,
)
from game_world.api.v1.views.game_world_story import (
    GameWorldStoryCreateAPIView,
    GameWorldStoryDeleteAPIView,
    GameWorldStoryDetailAPIView,
    GameWorldStoryListAPIView,
    GameWorldStoryUpdateAPIView,
)
from game_world.api.v1.views.mission import (
    MissionCreateAPIView,
    MissionDeleteAPIView,
    MissionDetailAPIView,
    MissionListAPIView,
    MissionUpdateAPIView,
)
from game_world.api.v1.views.mission_artifact import (
    MissionArtifactCreateAPIView,
    MissionArtifactDeleteAPIView,
    MissionArtifactDetailAPIView,
    MissionArtifactListAPIView,
    MissionArtifactUpdateAPIView,
)
from game_world.api.v1.views.mission_branch import (
    MissionBranchCreateAPIView,
    MissionBranchDeleteAPIView,
    MissionBranchDetailAPIView,
    MissionBranchListAPIView,
    MissionBranchUpdateAPIView,
)
from game_world.api.v1.views.mission_competency import (
    MissionCompetencyCreateAPIView,
    MissionCompetencyDeleteAPIView,
    MissionCompetencyDetailAPIView,
    MissionCompetencyListAPIView,
    MissionCompetencyUpdateAPIView,
)
from game_world.api.v1.views.mission_level import (
    MissionLevelCreateAPIView,
    MissionLevelDeleteAPIView,
    MissionLevelDetailAPIView,
    MissionLevelListAPIView,
    MissionLevelUpdateAPIView,
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
    "EventCheckQrCodeAPIView",
    # GameWorld
    "GameWorldListAPIView",
    "GameWorldDetailAPIView",
    "GameWorldCreateAPIView",
    "GameWorldUpdateAPIView",
    "GameWorldDeleteAPIView",
    "GameWorldStatisticsAPIView",
    "GameWorldGenerateAPIView",
    "GameWorldInfoForGenerateAPIView",
    "GameWorldDataForGraphAPIView",
    "GameWorldUpdateOrCreateAllEntitiesAPIView",
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
    # MissionLevel
    "MissionLevelListAPIView",
    "MissionLevelDetailAPIView",
    "MissionLevelCreateAPIView",
    "MissionLevelUpdateAPIView",
    "MissionLevelDeleteAPIView",
    # MissionCompetency
    "MissionCompetencyListAPIView",
    "MissionCompetencyDetailAPIView",
    "MissionCompetencyCreateAPIView",
    "MissionCompetencyUpdateAPIView",
    "MissionCompetencyDeleteAPIView",
    # MissionArtifact
    "MissionArtifactListAPIView",
    "MissionArtifactDetailAPIView",
    "MissionArtifactCreateAPIView",
    "MissionArtifactUpdateAPIView",
    "MissionArtifactDeleteAPIView",
    # GameWorldStory
    "GameWorldStoryListAPIView",
    "GameWorldStoryDetailAPIView",
    "GameWorldStoryCreateAPIView",
    "GameWorldStoryUpdateAPIView",
    "GameWorldStoryDeleteAPIView",
    # EventCompetency
    "EventCompetencyListAPIView",
    "EventCompetencyDetailAPIView",
    "EventCompetencyCreateAPIView",
    "EventCompetencyUpdateAPIView",
    "EventCompetencyDeleteAPIView",
    # EventArtifact
    "EventArtifactListAPIView",
    "EventArtifactDetailAPIView",
    "EventArtifactCreateAPIView",
    "EventArtifactUpdateAPIView",
    "EventArtifactDeleteAPIView",
)
