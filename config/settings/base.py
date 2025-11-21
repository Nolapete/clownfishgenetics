import os
from pathlib import Path

import environ
from oscar.defaults import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {"default": env.db()}

WHOOSH_INDEX_PATH = os.path.join(BASE_DIR, "whoosh_index")

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": WHOOSH_INDEX_PATH,
    },
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.flatpages",
    "django.contrib.sites",
    "django.contrib.postgres",
    # Third party apps
    "rest_framework",
    "ninja",
    "django_htmx",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "waffle",
    "oscar.config.Shop",
    "oscar.apps.analytics.apps.AnalyticsConfig",
    "oscar.apps.checkout.apps.CheckoutConfig",
    "oscar.apps.address.apps.AddressConfig",
    "oscar.apps.shipping.apps.ShippingConfig",
    "oscar.apps.catalogue.apps.CatalogueConfig",
    "oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig",
    "oscar.apps.communication.apps.CommunicationConfig",
    "oscar.apps.partner.apps.PartnerConfig",
    "oscar.apps.basket.apps.BasketConfig",
    "oscar.apps.payment.apps.PaymentConfig",
    "oscar.apps.offer.apps.OfferConfig",
    "oscar.apps.order.apps.OrderConfig",
    "oscar.apps.customer.apps.CustomerConfig",
    "oscar.apps.search.apps.SearchConfig",
    "oscar.apps.voucher.apps.VoucherConfig",
    "oscar.apps.wishlists.apps.WishlistsConfig",
    "oscar.apps.dashboard.apps.DashboardConfig",
    "oscar.apps.dashboard.reports.apps.ReportsDashboardConfig",
    "oscar.apps.dashboard.users.apps.UsersDashboardConfig",
    "oscar.apps.dashboard.orders.apps.OrdersDashboardConfig",
    "oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig",
    "oscar.apps.dashboard.offers.apps.OffersDashboardConfig",
    "oscar.apps.dashboard.partners.apps.PartnersDashboardConfig",
    "oscar.apps.dashboard.pages.apps.PagesDashboardConfig",
    "oscar.apps.dashboard.ranges.apps.RangesDashboardConfig",
    "oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig",
    "oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig",
    "oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig",
    "oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig",
    "crm",
    "django_celery_results",
    "widget_tweaks",
    "haystack",
    "treebeard",
    "sorl.thumbnail",
    "django_tables2",
    # Apps
    "landing",
    "calculator",
    "calcRefactor",
    "genetics_manager",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "config.middleware.LoginRequiredMiddleware",
    "oscar.apps.basket.middleware.BasketMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Allow unauthenticated access to these paths; everything else requires login
LOGIN_REQUIRED_EXEMPT_URLS = [
    r"^accounts/.*",  # allauth: login, signup, password reset,
    # email confirm, social callbacks
    r"^admin/login/$",  # allow admin login
    r"^static/.*",  # static assets
    r"^media/.*",  # media files (if served by Django)
    r"^api/.*",  # let DRF permission classes handle API auth
]

# Allauth provider defaults (tweak as needed per provider docs)
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["email", "profile"],
        "AUTH_PARAMS": {"prompt": "select_account"},
    },
    "github": {
        "SCOPE": ["user:email"],
    },
}

SOCIALACCOUNT_LOGIN_ON_GET = True


WSGI_APPLICATION = "config.wsgi.application"

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"

# DRF: default to authenticated; public endpoints can override with AllowAny
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# For production deployment
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_collected")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Django Oscar Settings (Minimum Requirements)
OSCAR_SHOP_NAME = "Clownfish Breeders Resource"
OSCAR_FROM_EMAIL = "support@clownfishgenetics.org"
SITE_ID = 1  # Required by Allauth and Oscar
# Optional: Set the user model if Oscar doesn't find it automatically
OSCAR_USER_MODEL = "auth.User"
