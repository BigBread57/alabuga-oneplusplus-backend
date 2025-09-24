from django.urls import path

from user.api.v1.views import (
    CharacterActualForUserAPIView,
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

app_name = "v1"


user_urls = [
    path(
        route="users/resend-email-confirmation/",
        view=UseResendEmailConfirmationAPIView.as_view(),
        name="users-resend-email-confirmation",
    ),
    path(
        route="users/login/",
        view=UserLoginAPIView.as_view(),
        name="users-login",
    ),
    path(
        route="users/request-reset-password/",
        view=UserRequestResetPasswordAPIView.as_view(),
        name="users-request-reset-password",
    ),
    path(
        route="users/confirm-reset-password/<path:extra_path>/",
        view=UserConfirmResetPasswordAPIView.as_view(),
        name="users-confirm-reset-password",
    ),
    path(
        route="users/update-password/",
        view=UserUpdatePasswordAPIView.as_view(),
        name="users-update-password",
    ),
    path(
        route="users/register/",
        view=UserRegisterAPIView.as_view(),
        name="users-register",
    ),
    path(
        route="users/logout/",
        view=UserLogoutAPIView.as_view(),
        name="users-logout",
    ),
    path(
        route="users/info/",
        view=UserInfoAPIView.as_view(),
        name="users-info",
    ),
    path(
        route="users/confirm-register/<path:extra_path>",
        view=UserConfirmRegisterAPIView.as_view(),
        name="users-confirm-register",
    ),
]

character_urls = [
    path(
        route="characters/actual-for-user/",
        view=CharacterActualForUserAPIView.as_view(),
        name="characters-actual-for-user",
    ),
]


urlpatterns = [
    *user_urls,
    *character_urls,
]
