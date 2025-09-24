from user.api.v1.views.character import CharacterActualForUserAPIView
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
    "UseResendEmailConfirmationAPIView",
    "UserLoginAPIView",
    "UserRequestResetPasswordAPIView",
    "UserConfirmResetPasswordAPIView",
    "UserUpdatePasswordAPIView",
    "UserRegisterAPIView",
    "UserLogoutAPIView",
    "UserInfoAPIView",
    "UserConfirmRegisterAPIView",
    "CharacterActualForUserAPIView",
)
