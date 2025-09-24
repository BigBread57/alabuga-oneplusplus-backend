from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.providers.keycloak import oauth2_callback, oauth2_login

urlpatterns = [
    # Admin.
    path("admin/doc/", include(admindocs_urls)),
    path("admin/", admin.site.urls),
    # API.
    path("api/", include("user.api.urls")),
    path("api/", include("shop.api.urls")),
    # Docs.
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("accounts/", include("allauth.urls")),  # тут будет login/logout/signup
    path("accounts/keycloak/login/", oauth2_login, name="keycloak_login"),
    path("accounts/keycloak/login/callback/", oauth2_callback, name="keycloak_callback"),
]


if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static

    urlpatterns = [
        *urlpatterns,
        *debug_toolbar_urls(),
        *static(
            # Serving media files in development only:
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        ),
    ]
