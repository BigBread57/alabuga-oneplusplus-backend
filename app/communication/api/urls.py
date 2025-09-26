from django.urls import include, path

app_name = "communication"


urlpatterns = [
    path("v1/communication/", include("communication.api.v1.urls")),
]
