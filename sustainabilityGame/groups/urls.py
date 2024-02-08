from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create, name="create"),
    path("join/", views.join, name="join"),

]