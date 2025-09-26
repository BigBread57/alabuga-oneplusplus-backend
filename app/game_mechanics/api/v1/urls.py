from django.urls import path

from game_mechanics.api.v1 import views

app_name = "v1"


competency_urls = [
    path(
        route="competencies/list/",
        view=views.CompetencyListAPIView.as_view(),
        name="competencies-list",
    ),
    path(
        route="competencies/create/",
        view=views.CompetencyCreateAPIView.as_view(),
        name="competencies-create",
    ),
    path(
        route="competencies/<int:pk>/update/",
        view=views.CompetencyUpdateAPIView.as_view(),
        name="competencies-update",
    ),
    path(
        route="competencies/<int:pk>/delete/",
        view=views.CompetencyDeleteAPIView.as_view(),
        name="competencies-delete",
    ),
]

rank_urls = [
    path(
        route="ranks/list/",
        view=views.RankListAPIView.as_view(),
        name="ranks-list",
    ),
    path(
        route="ranks/create/",
        view=views.RankCreateAPIView.as_view(),
        name="ranks-create",
    ),
    path(
        route="ranks/<int:pk>/update/",
        view=views.RankUpdateAPIView.as_view(),
        name="ranks-update",
    ),
    path(
        route="ranks/<int:pk>/delete/",
        view=views.RankDeleteAPIView.as_view(),
        name="ranks-delete",
    ),
]

required_rank_competency_urls = [
    path(
        route="required-rank-competencies/list/",
        view=views.RequiredRankCompetencyListAPIView.as_view(),
        name="required-rank-competencies-list",
    ),
    path(
        route="required-rank-competencies/create/",
        view=views.RequiredRankCompetencyCreateAPIView.as_view(),
        name="required-rank-competencies-create",
    ),
    path(
        route="required-rank-competencies/<int:pk>/update/",
        view=views.RequiredRankCompetencyUpdateAPIView.as_view(),
        name="required-rank-competencies-update",
    ),
    path(
        route="required-rank-competencies/<int:pk>/delete/",
        view=views.RequiredRankCompetencyDeleteAPIView.as_view(),
        name="required-rank-competencies-delete",
    ),
]


urlpatterns = [
    *competency_urls,
    *rank_urls,
    *required_rank_competency_urls,
]
