from django.urls import path

from multimedia.api.v1.views import MultimediaCreateAPIView

app_name = "v1"


multimedia_urls = [
    path(
        route="multimedias/create/",
        view=MultimediaCreateAPIView.as_view(),
        name="multimedias-create",
    ),
]


urlpatterns = [
    *multimedia_urls,
]
