from django.urls import include, path

app_name = "game_world"


urlpatterns = [
    path("v1/game-world/", include("game_world.api.v1.urls")),
]
