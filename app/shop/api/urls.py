from django.urls import include, path

app_name = "shop"


urlpatterns = [
    path("v1/shop/", include("shop.api.v1.urls")),
]
