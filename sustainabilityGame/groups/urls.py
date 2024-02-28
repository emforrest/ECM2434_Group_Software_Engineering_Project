from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_group, name="create_group"),
    path('join/', views.join_group, name='join_group'),
    path('leave/', views.leave_group, name='leave_group'),
]
