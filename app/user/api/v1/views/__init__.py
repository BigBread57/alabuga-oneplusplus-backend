from user.api.v1.views.character import CharacterActualForUserAPIView
from user.api.v1.views.character_artifact import CharacterArtifactListAPIView, CharacterArtifactDetailAPIView
from user.api.v1.views.character_competency import CharacterCompetencyListAPIView, CharacterCompetencyDetailAPIView
from user.api.v1.views.character_event import (
    CharacterEventUpdateFromCharacterAPIView,
    CharacterEventUpdateFromInspectorAPIView, CharacterEventListAPIView, CharacterEventDetailAPIView,
)
from user.api.v1.views.character_mission import (
    CharacterMissionUpdateFromCharacterAPIView,
    CharacterMissionUpdateFromInspectorAPIView, CharacterMissionListAPIView, CharacterMissionDetailAPIView,
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
