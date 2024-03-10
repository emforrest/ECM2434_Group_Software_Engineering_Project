"""Defines the URL patterns beginning /user/ and links them to a function within views.py

Authors:
- Eleanor Forrest
- Sam Townley
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("settings/", views.settings, name="settings"),
    path("journeys/<int:journey_id>/", views.journey_created, name="success"),
    path("journeys/create", views.start_journey, name="start"),
    path("journeys/finish", views.end_journey, name="end")
]