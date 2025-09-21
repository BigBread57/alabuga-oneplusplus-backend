from django.urls import include, path

app_name = "game_mechanics"


urlpatterns = [
    path("v1/game-mechanics/", include("game_mechanics.api.v1.urls")),
]
