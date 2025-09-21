from django.urls import path

from app.game_mechanics.api.v1.views import (
    ArtifactListAPIView,
    ArtifactCreateAPIView,
    ArtifactUpdateAPIView,
    ArtifactDeleteAPIView,
    CompetencyListAPIView,
    CompetencyCreateAPIView,
    CompetencyUpdateAPIView,
    CompetencyDeleteAPIView,
    RequiredRankCompetencyListAPIView,
    RankCreateAPIView,
    RankUpdateAPIView,
    RankDeleteAPIView,
    RequiredRankCompetencyCreateAPIView,
    RequiredRankCompetencyUpdateAPIView,
    RequiredRankCompetencyDeleteAPIView,
    RankListAPIView,
)

app_name = "v1"


artifact_urls = [
    path(
        route="artifacts/list/",
        view=ArtifactListAPIView.as_view(),
        name="artifacts-list",
    ),
    path(
        route="artifacts/create/",
        view=ArtifactCreateAPIView.as_view(),
        name="artifacts-create",
    ),
    path(
        route="artifacts/<int:pk>/update/",
        view=ArtifactUpdateAPIView.as_view(),
        name="artifacts-update",
    ),
    path(
        route="artifacts/<int:pk>/delete/",
        view=ArtifactDeleteAPIView.as_view(),
        name="artifacts-delete",
    ),
]

competency_urls = [
    path(
        route="competencies/list/",
        view=CompetencyListAPIView.as_view(),
        name="competencies-list",
    ),
    path(
        route="competencies/create/",
        view=CompetencyCreateAPIView.as_view(),
        name="competencies-create",
    ),
    path(
        route="competencies/<int:pk>/update/",
        view=CompetencyUpdateAPIView.as_view(),
        name="competencies-update",
    ),
    path(
        route="competencies/<int:pk>/delete/",
        view=CompetencyDeleteAPIView.as_view(),
        name="competencies-delete",
    ),
]

rank_urls = [
    path(
        route="ranks/list/",
        view=RankListAPIView.as_view(),
        name="ranks-list",
    ),
    path(
        route="ranks/create/",
        view=RankCreateAPIView.as_view(),
        name="ranks-create",
    ),
    path(
        route="ranks/<int:pk>/update/",
        view=RankUpdateAPIView.as_view(),
        name="ranks-update",
    ),
    path(
        route="ranks/<int:pk>/delete/",
        view=RankDeleteAPIView.as_view(),
        name="ranks-delete",
    ),
]

required_rank_competency_urls = [
    path(
        route="required-rank-competencies/list/",
        view=RequiredRankCompetencyListAPIView.as_view(),
        name="required-rank-competencies-list",
    ),
    path(
        route="required-rank-competencies/create/",
        view=RequiredRankCompetencyCreateAPIView.as_view(),
        name="required-rank-competencies-create",
    ),
    path(
        route="required-rank-competencies/<int:pk>/update/",
        view=RequiredRankCompetencyUpdateAPIView.as_view(),
        name="required-rank-competencies-update",
    ),
    path(
        route="required-rank-competencies/<int:pk>/delete/",
        view=RequiredRankCompetencyDeleteAPIView.as_view(),
        name="required-rank-competencies-delete",
    ),
]


urlpatterns = [
    *artifact_urls,
    *competency_urls,
    *rank_urls,
    *required_rank_competency_urls,
]
