from app.game_mechanics.api.v1.serializers.artifact import (
    ArtifactListSerializer,
    ArtifactCreateOrUpdateSerializer,
    ArtifactDetailSerializer,
)
from app.game_mechanics.api.v1.serializers.competency import (
    CompetencyListSerializer,
    CompetencyDetailSerializer,
    CompetencyCreateOrUpdateSerializer,
)
from app.game_mechanics.api.v1.serializers.rank import (
    RankListSerializer,
    RankDetailSerializer,
    RankCreateOrUpdateSerializer,
)
from app.game_mechanics.api.v1.serializers.required_rank_competency import (
    RequiredRankCompetencyListSerializer,
    RequiredRankCompetencyDetailSerializer,
    RequiredRankCompetencyCreateOrUpdateSerializer,
)


__all__ = (
    # Artifact
    "ArtifactListSerializer",
    "ArtifactDetailSerializer",
    "ArtifactCreateOrUpdateSerializer",
    # Competency
    "CompetencyListSerializer",
    "CompetencyDetailSerializer",
    "CompetencyCreateOrUpdateSerializer",
    # Rank
    "RankListSerializer",
    "RankDetailSerializer",
    "RankCreateOrUpdateSerializer",
    # RequiredRankCompetency
    "RequiredRankCompetencyListSerializer",
    "RequiredRankCompetencyDetailSerializer",
    "RequiredRankCompetencyCreateOrUpdateSerializer",
)
