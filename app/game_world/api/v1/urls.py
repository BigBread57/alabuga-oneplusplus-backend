from django.urls import path

from game_world.api.v1 import views

app_name = "v1"


artifact_urls = [
    path(
        route="artifacts/list/",
        view=views.ArtifactListAPIView.as_view(),
        name="artifacts-list",
    ),
    path(
        route="artifacts/create/",
        view=views.ArtifactCreateAPIView.as_view(),
        name="artifacts-create",
    ),
    path(
        route="artifacts/<int:pk>/update/",
        view=views.ArtifactUpdateAPIView.as_view(),
        name="artifacts-update",
    ),
    path(
        route="artifacts/<int:pk>/delete/",
        view=views.ArtifactDeleteAPIView.as_view(),
        name="artifacts-delete",
    ),
]

event_urls = [
    path(
        route="events/list/",
        view=views.EventListAPIView.as_view(),
        name="events-list",
    ),
    path(
        route="events/<int:pk>/detail/",
        view=views.EventDetailAPIView.as_view(),
        name="events-detail/",
    ),
    path(
        route="events/create/",
        view=views.EventCreateAPIView.as_view(),
        name="events-create",
    ),
    path(
        route="events/<int:pk>/update/",
        view=views.EventUpdateAPIView.as_view(),
        name="events-update",
    ),
    path(
        route="events/<int:pk>/delete/",
        view=views.EventDeleteAPIView.as_view(),
        name="events-delete",
    ),
    path(
        route="events/check-qr-code/",
        view=views.EventCheckQrCodeAPIView.as_view(),
        name="events-check-qr-code",
    ),
]

game_world_urls = [
    path(
        route="game-worlds/list/",
        view=views.GameWorldListAPIView.as_view(),
        name="game-worlds-list",
    ),
    path(
        route="game-worlds/<int:pk>/detail/",
        view=views.GameWorldDetailAPIView.as_view(),
        name="game-worlds-detail/",
    ),
    path(
        route="game-worlds/create/",
        view=views.GameWorldCreateAPIView.as_view(),
        name="game-worlds-create",
    ),
    path(
        route="game-worlds/<int:pk>/update/",
        view=views.GameWorldUpdateAPIView.as_view(),
        name="game-worlds-update",
    ),
    path(
        route="game-worlds/<int:pk>/delete/",
        view=views.GameWorldDeleteAPIView.as_view(),
        name="game-worlds-delete",
    ),
    path(
        route="game-worlds/<int:pk>/info-for-generate/",
        view=views.GameWorldInfoForGenerateAPIView.as_view(),
        name="game-worlds-info-for-generate",
    ),
    path(
        route="game-worlds/<int:pk>/generate/",
        view=views.GameWorldGenerateAPIView.as_view(),
        name="game-worlds-generate",
    ),
    path(
        route="game-worlds/<int:pk>/statistics/",
        view=views.GameWorldStatisticsAPIView.as_view(),
        name="game-worlds-statistics",
    ),
    path(
        route="game-worlds/<int:pk>/all-info/",
        view=views.GameWorldListWithAllEntitiesAPIView.as_view(),
        name="game-worlds-all-info",
    ),
]

mission_urls = [
    path(
        route="missions/list/",
        view=views.MissionListAPIView.as_view(),
        name="missions-list",
    ),
    path(
        route="missions/<int:pk>/detail/",
        view=views.MissionDetailAPIView.as_view(),
        name="missions-detail/",
    ),
    path(
        route="missions/create/",
        view=views.MissionCreateAPIView.as_view(),
        name="missions-create",
    ),
    path(
        route="missions/<int:pk>/update/",
        view=views.MissionUpdateAPIView.as_view(),
        name="missions-update",
    ),
    path(
        route="missions/<int:pk>/delete/",
        view=views.MissionDeleteAPIView.as_view(),
        name="missions-delete",
    ),
]

mission_branch_urls = [
    path(
        route="mission-branches/list/",
        view=views.MissionBranchListAPIView.as_view(),
        name="mission-branches-list",
    ),
    path(
        route="mission-branches/<int:pk>/detail/",
        view=views.MissionBranchDetailAPIView.as_view(),
        name="mission-branches-detail/",
    ),
    path(
        route="mission-branches/create/",
        view=views.MissionBranchCreateAPIView.as_view(),
        name="mission-branches-create",
    ),
    path(
        route="mission-branches/<int:pk>/update/",
        view=views.MissionBranchUpdateAPIView.as_view(),
        name="mission-branches-update",
    ),
    path(
        route="mission-branches/<int:pk>/delete/",
        view=views.MissionBranchDeleteAPIView.as_view(),
        name="mission-branches-delete",
    ),
]
activity_category_urls = [
    path(
        route="mission-categories/list/",
        view=views.ActivityCategoryListAPIView.as_view(),
        name="mission-categories-list",
    ),
    path(
        route="mission-categories/<int:pk>/detail/",
        view=views.ActivityCategoryDetailAPIView.as_view(),
        name="mission-categories-detail/",
    ),
    path(
        route="mission-categories/create/",
        view=views.ActivityCategoryCreateAPIView.as_view(),
        name="mission-categories-create",
    ),
    path(
        route="mission-categories/<int:pk>/update/",
        view=views.ActivityCategoryUpdateAPIView.as_view(),
        name="mission-categories-update",
    ),
    path(
        route="mission-categories/<int:pk>/delete/",
        view=views.ActivityCategoryDeleteAPIView.as_view(),
        name="mission-categories-delete",
    ),
]


# MissionLevel URLs
mission_level_urls = [
    path(
        route="mission-levels/list/",
        view=views.MissionLevelListAPIView.as_view(),
        name="mission-levels-list",
    ),
    path(
        route="mission-levels/<int:pk>/detail/",
        view=views.MissionLevelDetailAPIView.as_view(),
        name="mission-levels-detail",
    ),
    path(
        route="mission-levels/create/",
        view=views.MissionLevelCreateAPIView.as_view(),
        name="mission-levels-create",
    ),
    path(
        route="mission-levels/<int:pk>/update/",
        view=views.MissionLevelUpdateAPIView.as_view(),
        name="mission-levels-update",
    ),
    path(
        route="mission-levels/<int:pk>/delete/",
        view=views.MissionLevelDeleteAPIView.as_view(),
        name="mission-levels-delete",
    ),
]

# MissionCompetency URLs
mission_competency_urls = [
    path(
        route="mission-competencies/list/",
        view=views.MissionCompetencyListAPIView.as_view(),
        name="mission-competencies-list",
    ),
    path(
        route="mission-competencies/<int:pk>/detail/",
        view=views.MissionCompetencyDetailAPIView.as_view(),
        name="mission-competencies-detail",
    ),
    path(
        route="mission-competencies/create/",
        view=views.MissionCompetencyCreateAPIView.as_view(),
        name="mission-competencies-create",
    ),
    path(
        route="mission-competencies/<int:pk>/update/",
        view=views.MissionCompetencyUpdateAPIView.as_view(),
        name="mission-competencies-update",
    ),
    path(
        route="mission-competencies/<int:pk>/delete/",
        view=views.MissionCompetencyDeleteAPIView.as_view(),
        name="mission-competencies-delete",
    ),
]

# MissionArtifact URLs
mission_artifact_urls = [
    path(
        route="mission-artifacts/list/",
        view=views.MissionArtifactListAPIView.as_view(),
        name="mission-artifacts-list",
    ),
    path(
        route="mission-artifacts/<int:pk>/detail/",
        view=views.MissionArtifactDetailAPIView.as_view(),
        name="mission-artifacts-detail",
    ),
    path(
        route="mission-artifacts/create/",
        view=views.MissionArtifactCreateAPIView.as_view(),
        name="mission-artifacts-create",
    ),
    path(
        route="mission-artifacts/<int:pk>/update/",
        view=views.MissionArtifactUpdateAPIView.as_view(),
        name="mission-artifacts-update",
    ),
    path(
        route="mission-artifacts/<int:pk>/delete/",
        view=views.MissionArtifactDeleteAPIView.as_view(),
        name="mission-artifacts-delete",
    ),
]

# GameWorldStory URLs
game_world_story_urls = [
    path(
        route="game-world-stories/list/",
        view=views.GameWorldStoryListAPIView.as_view(),
        name="game-world-stories-list",
    ),
    path(
        route="game-world-stories/<int:pk>/detail/",
        view=views.GameWorldStoryDetailAPIView.as_view(),
        name="game-world-stories-detail",
    ),
    path(
        route="game-world-stories/create/",
        view=views.GameWorldStoryCreateAPIView.as_view(),
        name="game-world-stories-create",
    ),
    path(
        route="game-world-stories/<int:pk>/update/",
        view=views.GameWorldStoryUpdateAPIView.as_view(),
        name="game-world-stories-update",
    ),
    path(
        route="game-world-stories/<int:pk>/delete/",
        view=views.GameWorldStoryDeleteAPIView.as_view(),
        name="game-world-stories-delete",
    ),
]

# EventCompetency URLs
event_competency_urls = [
    path(
        route="event-competencies/list/",
        view=views.EventCompetencyListAPIView.as_view(),
        name="event-competencies-list",
    ),
    path(
        route="event-competencies/<int:pk>/detail/",
        view=views.EventCompetencyDetailAPIView.as_view(),
        name="event-competencies-detail",
    ),
    path(
        route="event-competencies/create/",
        view=views.EventCompetencyCreateAPIView.as_view(),
        name="event-competencies-create",
    ),
    path(
        route="event-competencies/<int:pk>/update/",
        view=views.EventCompetencyUpdateAPIView.as_view(),
        name="event-competencies-update",
    ),
    path(
        route="event-competencies/<int:pk>/delete/",
        view=views.EventCompetencyDeleteAPIView.as_view(),
        name="event-competencies-delete",
    ),
]

# EventArtifact URLs
event_artifact_urls = [
    path(
        route="event-artifacts/list/",
        view=views.EventArtifactListAPIView.as_view(),
        name="event-artifacts-list",
    ),
    path(
        route="event-artifacts/<int:pk>/detail/",
        view=views.EventArtifactDetailAPIView.as_view(),
        name="event-artifacts-detail",
    ),
    path(
        route="event-artifacts/create/",
        view=views.EventArtifactCreateAPIView.as_view(),
        name="event-artifacts-create",
    ),
    path(
        route="event-artifacts/<int:pk>/update/",
        view=views.EventArtifactUpdateAPIView.as_view(),
        name="event-artifacts-update",
    ),
    path(
        route="event-artifacts/<int:pk>/delete/",
        view=views.EventArtifactDeleteAPIView.as_view(),
        name="event-artifacts-delete",
    ),
]

urlpatterns = [
    *artifact_urls,
    *event_urls,
    *game_world_urls,
    *mission_urls,
    *mission_branch_urls,
    *activity_category_urls,
    *mission_level_urls,
    *mission_competency_urls,
    *mission_artifact_urls,
    *game_world_story_urls,
    *event_competency_urls,
    *event_artifact_urls,
]
