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
        route="game-worlds/rating/",
        view=views.GameWorldRatingAPIView.as_view(),
        name="game-worlds-rating",
    ),
    path(
        route="game-worlds/statistics/",
        view=views.GameWorldStatisticsAPIView.as_view(),
        name="game-worlds-statistics",
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

urlpatterns = [
    *artifact_urls,
    *event_urls,
    *game_world_urls,
    *mission_urls,
    *mission_branch_urls,
    *activity_category_urls,
]
