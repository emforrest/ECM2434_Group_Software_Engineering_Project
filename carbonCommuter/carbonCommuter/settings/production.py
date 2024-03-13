import os

# Basic configuration for the production environment
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get('DJANGO_SECRET')
DEBUG = False
ALLOWED_HOSTS = [".carboncommuter.xyz"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "sustainabilitygame",
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": "127.0.0.1",
        "PORT": os.environ.get("DB_PORT"),
    }
}


# Enforce HTTPS
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/#https

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True