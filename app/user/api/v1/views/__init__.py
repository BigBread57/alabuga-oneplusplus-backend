from user.api.v1.views.character import (
    CharacterActualForUserAPIView,
    CharacterActualUpdateAPIView,
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
    CharacterEventUpdateFromCharacterAPIView,
    CharacterEventUpdateFromInspectorAPIView,
)
from user.api.v1.views.character_mission import (
    CharacterMissionDetailAPIView,
    CharacterMissionListAPIView,
    CharacterMissionUpdateFromCharacterAPIView,
    CharacterMissionUpdateFromInspectorAPIView,
)
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

__all__ = (
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
    # CharacterEvent
    "CharacterEventListAPIView",
    "CharacterEventDetailAPIView",
    "CharacterEventUpdateFromCharacterAPIView",
    "CharacterEventUpdateFromInspectorAPIView",
    # CharacterMission
    "CharacterMissionListAPIView",
    "CharacterMissionDetailAPIView",
    "CharacterMissionUpdateFromCharacterAPIView",
    "CharacterMissionUpdateFromInspectorAPIView",
    # CharacterCompetency
    "CharacterCompetencyListAPIView",
    "CharacterCompetencyDetailAPIView",
    # CharacterArtifact
    "CharacterArtifactListAPIView",
    "CharacterArtifactDetailAPIView",
)
