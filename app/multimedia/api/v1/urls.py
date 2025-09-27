from django.urls import path

from multimedia.api.v1.views import MultimediaCreateAPIView

app_name = "v1"


multimedia_urls = [
    path(
        route="multimedia/create/",
        view=MultimediaCreateAPIView.as_view(),
        name="multimedia-create",
    ),
]


urlpatterns = [
    *multimedia_urls,
]
