from django.urls import path

from user.api.v1 import views

app_name = "v1"


user_urls = [
    path(
        route="users/resend-email-confirmation/",
        view=views.UseResendEmailConfirmationAPIView.as_view(),
        name="users-resend-email-confirmation",
    ),
    path(
        route="users/login/",
        view=views.UserLoginAPIView.as_view(),
        name="users-login",
    ),
    path(
        route="users/request-reset-password/",
        view=views.UserRequestResetPasswordAPIView.as_view(),
        name="users-request-reset-password",
    ),
    path(
        route="users/confirm-reset-password/<path:extra_path>/",
        view=views.UserConfirmResetPasswordAPIView.as_view(),
        name="users-confirm-reset-password",
    ),
    path(
        route="users/update-password/",
        view=views.UserUpdatePasswordAPIView.as_view(),
        name="users-update-password",
    ),
    path(
        route="users/register/",
        view=views.UserRegisterAPIView.as_view(),
        name="users-register",
    ),
    path(
        route="users/confirm-register/",
        view=views.UserConfirmRegisterAPIView.as_view(),
        name="users-confirm-register",
    ),
    path(
        route="users/logout/",
        view=views.UserLogoutAPIView.as_view(),
        name="users-logout",
    ),
    path(
        route="users/info/",
        view=views.UserInfoAPIView.as_view(),
        name="users-info",
    ),
]

character_urls = [
    path(
        route="characters/actual/",
        view=views.CharacterActualForUserAPIView.as_view(),
        name="characters-actual",
    ),
    path(
        route="characters/<int:pk>/statistics/",
        view=views.CharacterStatisticsAPIView.as_view(),
        name="characters-statistics",
    ),
    path(
        route="characters/actual/update/",
        view=views.CharacterActualUpdateAPIView.as_view(),
        name="characters-actual-update",
    ),
]

character_competency_urls = [
    path(
        route="character-competencies/list/",
        view=views.CharacterCompetencyListAPIView.as_view(),
        name="character-competencies-list",
    ),
    path(
        route="character-competencies/<int:pk>/detail/",
        view=views.CharacterCompetencyDetailAPIView.as_view(),
        name="character-competencies-detail",
    ),
]


character_artifact_urls = [
    path(
        route="character-artifacts/list/",
        view=views.CharacterArtifactListAPIView.as_view(),
        name="character-artifacts-list",
    ),
    path(
        route="character-artifacts/<int:pk>/detail/",
        view=views.CharacterArtifactDetailAPIView.as_view(),
        name="character-artifacts-detail",
    ),
]

character_event_urls = [
    path(
        route="character-events/list/",
        view=views.CharacterEventListAPIView.as_view(),
        name="character-events-list",
    ),
    path(
        route="character-events/<int:pk>/detail/",
        view=views.CharacterEventDetailAPIView.as_view(),
        name="character-events-detail",
    ),
    path(
        route="character-events/<int:pk>/update-for-character/",
        view=views.CharacterEventUpdateFromCharacterAPIView.as_view(),
        name="character-events-update-for-character",
    ),
    path(
        route="character-events/<int:pk>/update-for-inspector/",
        view=views.CharacterEventUpdateFromInspectorAPIView.as_view(),
        name="character-events-update-for-inspector",
    ),
]

character_mission_urls = [
    path(
        route="character-missions/list/",
        view=views.CharacterMissionListAPIView.as_view(),
        name="character-missions-list",
    ),
    path(
        route="character-missions/<int:pk>/detail/",
        view=views.CharacterMissionDetailAPIView.as_view(),
        name="character-missions-detail",
    ),
    path(
        route="character-missions/<int:pk>/update-for-character/",
        view=views.CharacterMissionUpdateFromCharacterAPIView.as_view(),
        name="character-missions-update-for-character",
    ),
    path(
        route="character-missions/<int:pk>/update-for-inspector/",
        view=views.CharacterMissionUpdateFromInspectorAPIView.as_view(),
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
