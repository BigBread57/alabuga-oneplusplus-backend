from django.urls import path

from user.api.v1.views import (
    CharacterActualForUserAPIView,
    CharacterEventUpdateFromCharacterAPIView,
    CharacterEventUpdateFromInspectorAPIView,
    CharacterMissionUpdateFromCharacterAPIView,
    CharacterMissionUpdateFromInspectorAPIView,
    UserConfirmRegisterAPIView,
    UserConfirmResetPasswordAPIView,
    UseResendEmailConfirmationAPIView,
    UserInfoAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserRegisterAPIView,
    UserRequestResetPasswordAPIView,
    UserUpdatePasswordAPIView, CharacterEventListAPIView, CharacterEventDetailAPIView, CharacterMissionListAPIView,
    CharacterMissionDetailAPIView, CharacterArtifactDetailAPIView, CharacterArtifactListAPIView,
    CharacterCompetencyDetailAPIView, CharacterCompetencyListAPIView,
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
        route="users/confirm-register/",
        view=UserConfirmRegisterAPIView.as_view(),
        name="users-confirm-register",
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
]

character_urls = [
    path(
        route="characters/actual-for-user/",
        view=CharacterActualForUserAPIView.as_view(),
        name="characters-actual-for-user",
    ),
]

character_competency_urls = [
    path(
        route="character-competencies/list/",
        view=CharacterCompetencyListAPIView.as_view(),
        name="character-competencies-list",
    ),
    path(
        route="character-competencies/<int:pk>/detail/",
        view=CharacterCompetencyDetailAPIView.as_view(),
        name="character-competencies-detail",
    ),
]


character_artifact_urls = [
    path(
        route="character-artifacts/list/",
        view=CharacterArtifactListAPIView.as_view(),
        name="character-artifacts-list",
    ),
    path(
        route="character-artifacts/<int:pk>/detail/",
        view=CharacterArtifactDetailAPIView.as_view(),
        name="character-artifacts-detail",
    ),
]

character_event_urls = [
    path(
        route="character-events/list/",
        view=CharacterEventListAPIView.as_view(),
        name="character-events-list",
    ),
    path(
        route="character-events/<int:pk>/detail/",
        view=CharacterEventDetailAPIView.as_view(),
        name="character-events-detail",
    ),
    path(
        route="character-events/<int:pk>/update-for-character/",
        view=CharacterEventUpdateFromCharacterAPIView.as_view(),
        name="character-events-update-for-character",
    ),
    path(
        route="character-events/<int:pk>/update-for-inspector/",
        view=CharacterEventUpdateFromInspectorAPIView.as_view(),
        name="character-events-update-for-inspector",
    ),
]

character_mission_urls = [
    path(
        route="character-missions/list/",
        view=CharacterMissionListAPIView.as_view(),
        name="character-missions-list",
    ),
    path(
        route="character-missions/<int:pk>/detail/",
        view=CharacterMissionDetailAPIView.as_view(),
        name="character-missions-detail",
    ),
    path(
        route="character-missions/<int:pk>/update-for-character/",
        view=CharacterMissionUpdateFromCharacterAPIView.as_view(),
        name="character-missions-update-for-character",
    ),
    path(
        route="character-missions/<int:pk>/update-for-inspector/",
        view=CharacterMissionUpdateFromInspectorAPIView.as_view(),
        name="character-missions-update-for-inspector",
    ),
]

urlpatterns = [
    *user_urls,
    *character_urls,
    *character_event_urls,
    *character_competency_urls,
    *character_artifact_urls,
    *character_mission_urls,
]
