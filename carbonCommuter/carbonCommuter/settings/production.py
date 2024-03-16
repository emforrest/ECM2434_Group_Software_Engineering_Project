import os
import sentry_sdk

# Basic configuration for the production environment
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get('DJANGO_SECRET')
DEBUG = False
ALLOWED_HOSTS = ["www.carboncommuter.xyz", "carboncommuter.xyz", "127.0.0.1", "localhost", "129.153.205.30", "speed.cloudflare.com"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "sustainabilitygame",
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}


# Enforce HTTPS
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/#https

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ["https://carboncommuter.xyz", "https://www.carboncommuter.xyz"]


# Configure Sentry for error monitoring
# https://docs.sentry.io/platforms/python/integrations/django/

sentry_sdk.init(
    dsn = "https://839e41d4294bd406c9960b0167553428@o4506904711069696.ingest.us.sentry.io/4506904722931712",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    enable_tracing = True,
    traces_sample_rate = 1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate = 1.0,
)
