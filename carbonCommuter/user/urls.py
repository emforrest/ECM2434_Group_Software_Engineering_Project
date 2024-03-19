"""Defines the URL patterns beginning /user/ and links them to a function within views.py

Authors:
- Eleanor Forrest
- Sam Townley
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="dashboard"),
    path("settings/", views.settings, name="settings"),
    path("journeys/<int:journey_id>/", views.journey, name="journey"),
    path("journeys/create", views.start_journey, name="start"),
    path("journeys/finish", views.end_journey, name="end"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/", views.follow, name="follow"),
    path("journeys/delete", views.delete_journey, name="delete"),
]