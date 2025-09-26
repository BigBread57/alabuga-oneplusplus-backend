from django.urls import include, path

app_name = "user"


urlpatterns = [
    path("v1/user/", include("user.api.v1.urls")),
]
