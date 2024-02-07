from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),  #access with /login/register
    path("signIn/", views.signIn, name = "signIn"),  #access with /login/signIn
]