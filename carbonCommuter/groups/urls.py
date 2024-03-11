from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_groups_home_page, name="user_groups_home_page"),
    path('search/', views.search_groups, name='search_groups'),
    path('view/<int:group_id>/', views.group_page, name='group_page'),
    path('join/<int:group_id>/', views.join_group, name='join_group'),
    path('leave/<int:group_id>/', views.leave_group, name='leave_group'),
]
