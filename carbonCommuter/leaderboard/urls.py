from django.urls import path
from .models import Leaderboard_Entry

from . import views

urlpatterns = [
    path("", views.leaderboard, name="leaderboard"),  
    path("user_leaderboard", views.user_leaderboard, name ="user_leaderboard")
]