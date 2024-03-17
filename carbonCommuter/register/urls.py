from django.urls import path

from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("PrivacyPolicy", views.PrivacyPolicy, name="Privacy Policy"),
]