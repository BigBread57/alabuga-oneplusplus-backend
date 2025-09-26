from alabuga.settings import config
from alabuga.settings.django import INSTALLED_APPS, MIDDLEWARE

DEBUG_TOOLS = config("DEBUG_TOOLS", default=False, cast=bool)

if DEBUG_TOOLS:
    INSTALLED_APPS: list[str] = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE: list[str] = [
        *MIDDLEWARE,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "querycount.middleware.QueryCountMiddleware",
    ]
    INTERNAL_IPS = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
    ]
