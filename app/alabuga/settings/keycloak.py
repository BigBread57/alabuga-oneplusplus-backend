from alabuga.settings import config

CLIENT_ID = config(
    "CLIENT_ID",
    default="django-sso",  # произвольное название Client задается при созданиие Client
)
CLIENT_SECRET = config(
    "CLIENT_SECRET",
    default="PAZsKiK1tt4bCmz6CUzSKDWttFU5rZyD",  # на странице редактирование Client вкладка Credentials поле Secret
)
REALM_NAME = config("REALM_NAME", default="Django Integration")  # задается при создании Realm
KEYCLOAK_URL_BASE = config("KEYCLOAK_URL_BASE", default="http://localhost:8080/auth/")  # базой url Keycloak
KEYCLOAK_AUDIENCE = config("KEYCLOAK_AUDIENCE", default="account")  # область Client - про это поговорим ниже
KEYCLOAK_IS_CREATE = config(
    "KEYCLOAK_IS_CREATE",
    default=1,  # флаг управляет, логикой что если пользователь не найден, то создаем
)

SOCIALACCOUNT_PROVIDERS = {
    "keycloak": {
        "APP": {
            "client_id": CLIENT_ID,
            "secret": CLIENT_SECRET,
            "key": "",
        }
    }
}
