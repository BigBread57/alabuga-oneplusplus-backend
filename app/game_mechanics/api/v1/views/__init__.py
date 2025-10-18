from game_mechanics.api.v1.views.competency import (
    CompetencyCreateAPIView,
    CompetencyDeleteAPIView,
    CompetencyListAPIView,
    CompetencyListMaxLevelAPIView,
    CompetencyUpdateAPIView,
)
from game_mechanics.api.v1.views.rank import (
    RankCreateAPIView,
    RankDeleteAPIView,
    RankListAPIView,
    RankUpdateAPIView,
)
from game_mechanics.api.v1.views.required_rank_competency import (
    RequiredRankCompetencyCreateAPIView,
    RequiredRankCompetencyDeleteAPIView,
    RequiredRankCompetencyListAPIView,
    RequiredRankCompetencyUpdateAPIView,
)

__all__ = (
    # Competency
    "CompetencyListAPIView",
    "CompetencyListMaxLevelAPIView",
    "CompetencyCreateAPIView",
    "CompetencyUpdateAPIView",
    "CompetencyDeleteAPIView",
    # Rank
    "RankListAPIView",
    "RankCreateAPIView",
    "RankUpdateAPIView",
    "RankDeleteAPIView",
    # RequiredRankCompetency
    "RequiredRankCompetencyListAPIView",
    "RequiredRankCompetencyCreateAPIView",
    "RequiredRankCompetencyUpdateAPIView",
    "RequiredRankCompetencyDeleteAPIView",
)
