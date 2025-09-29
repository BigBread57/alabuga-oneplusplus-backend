from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class KeycloakProvider(OAuth2Provider):
    id = "keycloak"
    name = "Keycloak"

    def extract_uid(self, data):
        return str(data["sub"])

    def extract_common_fields(self, data):
        return {
            "username": data.get("preferred_username"),
            "email": data.get("email"),
            "first_name": data.get("given_name", ""),
            "last_name": data.get("family_name", ""),
        }


class KeycloakOAuth2Adapter(OAuth2Adapter):
    provider_id = "keycloak"

    access_token_url = "http://localhost:8080/realms/your-realm/protocol/openid-connect/token"
    authorize_url = "http://localhost:8080/realms/your-realm/protocol/openid-connect/auth"
    profile_url = "http://localhost:8080/realms/your-realm/protocol/openid-connect/userinfo"

    def complete_login(self, request, app, token, **kwargs):
        import requests

        headers = {"Authorization": f"Bearer {token.token}"}
        response = requests.get(self.profile_url, headers=headers)
        response.raise_for_status()
        extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(KeycloakOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(KeycloakOAuth2Adapter)
