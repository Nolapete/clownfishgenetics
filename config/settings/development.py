from .base import INSTALLED_APPS, MIDDLEWARE

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# This setting is REQUIRED for the toolbar to appear in the browser
INTERNAL_IPS = [
    "127.0.0.1",
]
