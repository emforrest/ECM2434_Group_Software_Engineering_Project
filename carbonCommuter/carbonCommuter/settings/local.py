import os

# Basic configuration for the local development environment

SECRET_KEY = 'django-insecure-jpdvh@2*xm2zlkf!i9bs9u55+8%_891p!g3jl%n8j36vm#_*^='
DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "sustainabilitygame",
        "USER": "django",
        "PASSWORD": "acf6Z4LeA85FF9gY!",
        "HOST": "129.153.205.30",
        "PORT": "3306",
    }
}