"""Defines the URL patterns beginning /admin/ and links them to a function within views.py

Authors:
- Eleanor Forrest
- Sam Townley
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.mainAdmin, name="mainAdmin"),
    path("chooseEvent/", views.chooseEvent, name = "chooseEvent"),
    path("confirmEvent/", views.confirmEvent, name="confirmEvent"),
    path("submitEvent/", views.submitEvent, name="submitEvent"),
    path("verify/", views.verify_suspicious_journey, name="suspiciousJourney"),
]