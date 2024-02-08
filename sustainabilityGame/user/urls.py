from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"), #./user/home
    path("settings/", views.settings, name="settings"),
    path("upload/", views.upload, name="upload"),
]