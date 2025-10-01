from user.api.v1.serializers.character import (
    CharacterActualForUserSerializer,
    CharacterStatisticsSerializer,
    CharacterUpdateSerializer,
)
from user.api.v1.serializers.character_artifact import (
    CharacterArtifactDetailSerializer,
    CharacterArtifactListSerializer,
)
from user.api.v1.serializers.character_competency import (
    CharacterCompetencyDetailSerializer,
    CharacterCompetencyListSerializer,
)
from user.api.v1.serializers.character_event import (
    CharacterEventDetailSerializer,
    CharacterEventListSerializer,
    CharacterEventUpdateForInspectorSerializer,
    CharacterEventUpdateFromCharacterSerializer,
)
from user.api.v1.serializers.character_mission import (
    CharacterMissionDetailSerializer,
    CharacterMissionListSerializer,
    CharacterMissionUpdateForInspectorSerializer,
    CharacterMissionUpdateFromCharacterSerializer,
)
from user.api.v1.serializers.character_mission_branch import (
    CharacterMissionBranchListSerializer,
)
from user.api.v1.serializers.user import (
    UserConfirmResetPasswordSerializer,
    UseResendEmailConfirmationSerializer,
    UserInfoSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserRequestResetPasswordSerializer,
    UserUpdatePasswordSerializer,
)

__all__ = (
    # CharacterEvent
    "CharacterEventUpdateFromCharacterSerializer",
    "CharacterEventUpdateForInspectorSerializer",
    "CharacterEventDetailSerializer",
    "CharacterEventListSerializer",
    # CharacterMission
    "CharacterMissionUpdateFromCharacterSerializer",
    "CharacterMissionUpdateForInspectorSerializer",
    "CharacterMissionDetailSerializer",
    "CharacterMissionListSerializer",
    # CharacterMissionBranch
    "CharacterMissionBranchListSerializer",
    # User
    "UserLoginSerializer",
    "UserConfirmResetPasswordSerializer",
    "UserRequestResetPasswordSerializer",
    "UserUpdatePasswordSerializer",
    "UserRegisterSerializer",
    "UserInfoSerializer",
    "UseResendEmailConfirmationSerializer",
    # Character
    "CharacterActualForUserSerializer",
    "CharacterUpdateSerializer",
    "CharacterStatisticsSerializer",
    # CharacterCompetency
    "CharacterCompetencyListSerializer",
    "CharacterCompetencyDetailSerializer",
    # CharacterArtifact
    "CharacterArtifactListSerializer",
    "CharacterArtifactDetailSerializer",
)
