from user.api.v1.views.character import (
    CharacterActualForUserAPIView,
    CharacterActualUpdateAPIView,
    CharacterListAPIView,
    CharacterStatisticsAPIView,
)
from user.api.v1.views.character_artifact import (
    CharacterArtifactDetailAPIView,
    CharacterArtifactListAPIView,
)
from user.api.v1.views.character_competency import (
    CharacterCompetencyDetailAPIView,
    CharacterCompetencyListAPIView,
)
from user.api.v1.views.character_event import (
    CharacterEventDetailAPIView,
    CharacterEventListAPIView,
    CharacterEventListForInspectorAPIView,
    CharacterEventUpdateForInspectorAPIView,
    CharacterEventUpdateFromCharacterAPIView,
)
from user.api.v1.views.character_mission import (
    CharacterMissionDetailAPIView,
    CharacterMissionListAPIView,
    CharacterMissionListForInspectorAPIView,
    CharacterMissionUpdateForInspectorAPIView,
    CharacterMissionUpdateFromCharacterAPIView,
)
from user.api.v1.views.character_mission_branch import CharacterMissionBranchListAPIView
from user.api.v1.views.user import (
    UserConfirmRegisterAPIView,
    UserConfirmResetPasswordAPIView,
    UseResendEmailConfirmationAPIView,
    UserInfoAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserRegisterAPIView,
    UserRequestResetPasswordAPIView,
    UserUpdatePasswordAPIView,
)

__all__ = [
    # User
    "UseResendEmailConfirmationAPIView",
    "UserLoginAPIView",
    "UserRequestResetPasswordAPIView",
    "UserConfirmResetPasswordAPIView",
    "UserUpdatePasswordAPIView",
    "UserRegisterAPIView",
    "UserLogoutAPIView",
    "UserInfoAPIView",
    "UserConfirmRegisterAPIView",
    # Character
    "CharacterActualForUserAPIView",
    "CharacterActualUpdateAPIView",
    "CharacterStatisticsAPIView",
    "CharacterListAPIView",
    # CharacterEvent
    "CharacterEventListAPIView",
    "CharacterEventDetailAPIView",
    "CharacterEventUpdateFromCharacterAPIView",
    "CharacterEventUpdateForInspectorAPIView",
    "CharacterEventListForInspectorAPIView",
    # CharacterMission
    "CharacterMissionListAPIView",
    "CharacterMissionDetailAPIView",
    "CharacterMissionUpdateFromCharacterAPIView",
    "CharacterMissionUpdateForInspectorAPIView",
    "CharacterMissionListForInspectorAPIView",
    # CharacterMissionBranch
    "CharacterMissionBranchListAPIView",
    # CharacterCompetency
    "CharacterCompetencyListAPIView",
    "CharacterCompetencyDetailAPIView",
    # CharacterArtifact
    "CharacterArtifactListAPIView",
    "CharacterArtifactDetailAPIView",
]
