"""Defines the URL patterns beginning /user/ and links them to a function within views.py

Authors:
- Eleanor Forrest
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("settings/", views.settings, name="settings"),
    path("upload/", views.upload, name="upload"),
    path("upload/<int:journey_id>/", views.upload_success, name="success"),
]