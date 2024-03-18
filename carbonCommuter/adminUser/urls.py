from django.urls import path

from . import views

urlpatterns = [
    path("", views.mainAdmin, name="mainAdmin"),
    path("chooseEvent/", views.chooseEvent, name = "chooseEvent"),
    path("confirmEvent/", views.confirmEvent, name="confirmEvent")

]