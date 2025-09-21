from app.game_mechanics.api.v1.views.artifact import (
    ArtifactListAPIView,
    ArtifactCreateAPIView,
    ArtifactUpdateAPIView,
    ArtifactDeleteAPIView,
)
from app.game_mechanics.api.v1.views.competency import (
    CompetencyListAPIView,
    CompetencyCreateAPIView,
    CompetencyUpdateAPIView,
    CompetencyDeleteAPIView,
)
from app.game_mechanics.api.v1.views.rank import (
    RankListAPIView,
    RankCreateAPIView,
    RankDeleteAPIView,
    RankUpdateAPIView,
)
from app.game_mechanics.api.v1.views.required_rank_competency import (
    RequiredRankCompetencyListAPIView,
    RequiredRankCompetencyCreateAPIView,
    RequiredRankCompetencyUpdateAPIView,
    RequiredRankCompetencyDeleteAPIView,
)

__all__ = (
    # Artifact
    "ArtifactListAPIView",
    "ArtifactCreateAPIView",
    "ArtifactUpdateAPIView",
    "ArtifactDeleteAPIView",
    # Competency
    "CompetencyListAPIView",
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
