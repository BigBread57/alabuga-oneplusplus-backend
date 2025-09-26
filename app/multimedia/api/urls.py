from django.urls import include, path

app_name = "multimedia"


urlpatterns = [
    path("v1/multimedia/", include("multimedia.api.v1.urls")),
]
