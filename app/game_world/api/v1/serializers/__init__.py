from game_world.api.v1.serializers.activity_category import (
    ActivityCategoryCreateOrUpdateSerializer,
    ActivityCategoryDetailSerializer,
    ActivityCategoryListSerializer,
)
from game_world.api.v1.serializers.artifact import (
    ArtifactCreateOrUpdateSerializer,
    ArtifactDetailSerializer,
    ArtifactListSerializer,
)
from game_world.api.v1.serializers.event import (
    EventCreateOrUpdateSerializer,
    EventDetailSerializer,
    EventListSerializer,
)
from game_world.api.v1.serializers.event_artifact import (
    EventArtifactCreateOrUpdateSerializer,
    EventArtifactDetailSerializer,
    EventArtifactListSerializer,
)
from game_world.api.v1.serializers.event_competency import (
    EventCompetencyCreateOrUpdateSerializer,
    EventCompetencyDetailSerializer,
    EventCompetencyListSerializer,
)
from game_world.api.v1.serializers.game_world import (
    GameWorldCreateOrUpdateSerializer,
    GameWorldDataAfterGenerateSerializer,
    GameWorldDetailSerializer,
    GameWorldGenerateSerializer,
    GameWorldGlobalStatisticsSerializer,
    GameWorldInfoForGenerateSerializer,
    GameWorldListSerializer,
    GameWorldStatisticsSerializer,
    GameWorldUpdateOrCreateAllEntitiesSerializer,
)
from game_world.api.v1.serializers.game_world_all_entites import (
    GameWorldListWithAllEntitiesSerializer,
)
from game_world.api.v1.serializers.game_world_story import (
    GameWorldStoryCreateOrUpdateSerializer,
    GameWorldStoryDetailSerializer,
    GameWorldStoryListSerializer,
)
from game_world.api.v1.serializers.mission import (
    MissionCreateOrUpdateSerializer,
    MissionDetailSerializer,
    MissionListSerializer,
)
from game_world.api.v1.serializers.mission_artifact import (
    MissionArtifactCreateOrUpdateSerializer,
    MissionArtifactDetailSerializer,
    MissionArtifactListSerializer,
)
from game_world.api.v1.serializers.mission_branch import (
    MissionBranchCreateOrUpdateSerializer,
    MissionBranchDetailSerializer,
    MissionBranchListSerializer,
)
from game_world.api.v1.serializers.mission_competency import (
    MissionCompetencyCreateOrUpdateSerializer,
    MissionCompetencyDetailSerializer,
    MissionCompetencyListSerializer,
)
from game_world.api.v1.serializers.mission_level import (
    MissionLevelCreateOrUpdateSerializer,
    MissionLevelDetailSerializer,
    MissionLevelListSerializer,
)

__all__ = (
    # Artifact
    "ArtifactListSerializer",
    "ArtifactDetailSerializer",
    "ArtifactCreateOrUpdateSerializer",
    # Event
    "EventListSerializer",
    "EventDetailSerializer",
    "EventCreateOrUpdateSerializer",
    # GameWorld
    "GameWorldListSerializer",
    "GameWorldDetailSerializer",
    "GameWorldCreateOrUpdateSerializer",
    "GameWorldGlobalStatisticsSerializer",
    "GameWorldStatisticsSerializer",
    "GameWorldInfoForGenerateSerializer",
    "GameWorldGenerateSerializer",
    "GameWorldDataAfterGenerateSerializer",
    "GameWorldUpdateOrCreateAllEntitiesSerializer",
    "GameWorldListWithAllEntitiesSerializer",
    # Mission
    "MissionListSerializer",
    "MissionDetailSerializer",
    "MissionCreateOrUpdateSerializer",
    # MissionBranch
    "MissionBranchListSerializer",
    "MissionBranchDetailSerializer",
    "MissionBranchCreateOrUpdateSerializer",
    # ActivityCategory
    "ActivityCategoryListSerializer",
    "ActivityCategoryDetailSerializer",
    "ActivityCategoryCreateOrUpdateSerializer",
    # MissionLevel
    "MissionLevelListSerializer",
    "MissionLevelDetailSerializer",
    "MissionLevelCreateOrUpdateSerializer",
    # MissionCompetency
    "MissionCompetencyListSerializer",
    "MissionCompetencyDetailSerializer",
    "MissionCompetencyCreateOrUpdateSerializer",
    # MissionArtifact
    "MissionArtifactListSerializer",
    "MissionArtifactDetailSerializer",
    "MissionArtifactCreateOrUpdateSerializer",
    # GameWorldStory
    "GameWorldStoryListSerializer",
    "GameWorldStoryDetailSerializer",
    "GameWorldStoryCreateOrUpdateSerializer",
    # EventCompetency
    "EventCompetencyListSerializer",
    "EventCompetencyDetailSerializer",
    "EventCompetencyCreateOrUpdateSerializer",
    # EventArtifact
    "EventArtifactListSerializer",
    "EventArtifactDetailSerializer",
    "EventArtifactCreateOrUpdateSerializer",
)
