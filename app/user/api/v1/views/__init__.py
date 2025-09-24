from user.api.v1.views.character import CharacterActualForUserAPIView
from user.api.v1.views.character_event import (
    CharacterEventUpdateFromCharacterAPIView,
    CharacterEventUpdateFromInspectorAPIView,
)
from user.api.v1.views.character_mission import (
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
    # CharacterEvent
    "CharacterEventUpdateFromCharacterAPIView",
    "CharacterEventUpdateFromInspectorAPIView",
    # CharacterMission
    "CharacterMissionUpdateFromCharacterAPIView",
    "CharacterMissionUpdateFromInspectorAPIView",
)
