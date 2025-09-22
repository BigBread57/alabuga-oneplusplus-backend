import os

from django.utils.translation import gettext_lazy as _

from app.alabuga.settings import BASE_DIR, config

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
SITE_ID = 1

BASE_INSTALLED_APPS: list[str] = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.admindocs",
]
OTHER_INSTALLED_APPS: list[str] = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.oauth2",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "rules",
    "drf_spectacular",
    "drf_standardized_errors",
    "django_kafka",
    "django_producer",
    "django_celery_beat",
    "s3_uploads",
    "catalog",
    "dynamic",
    "admin_auto_filters",
    "more_admin_filters",
    "safedelete",
]

LOCAL_INSTALLED_APPS: list[str] = [
    "core",
    "crm",
    "schedule",
    "individual_metering_device",
    "placement_status",
    "reference_book",
    "defect",
]


INSTALLED_APPS: list[str] = [
    *BASE_INSTALLED_APPS,
    *OTHER_INSTALLED_APPS,
    *LOCAL_INSTALLED_APPS,
]

MIDDLEWARE: list[str] = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "alabuga.urls"
WSGI_APPLICATION = "alabuga.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_DB", default="alabuga", cast=str),
        "USER": config("POSTGRES_USER", default="alabuga", cast=str),
        "PASSWORD": config("POSTGRES_PASSWORD", default="alabuga", cast=str),
        "HOST": config("DJANGO_DATABASE_HOST", default="localhost", cast=str),
        "PORT": config("DJANGO_DATABASE_PORT", default=5432, cast=int),
        "CONN_MAX_AGE": config("CONN_MAX_AGE", default=60, cast=int),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=30000",
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "ru-RU"

USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ("ru", _("Russian")),
    ("en", _("English")),
)

LOCALE_PATHS = ("locale/",)

USE_TZ = True
TIME_ZONE = "UTC"

TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.joinpath("alabuga", "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    }
]

AUTH_USER_MODEL = "user.User"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "files", "static")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "files", "media")

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

PASSWORD_HASHERS: list[str] = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]


if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
