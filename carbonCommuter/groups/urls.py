from django.urls import path
from . import views

urlpatterns = [
    # Home page for user groups
    path("", views.user_groups_home_page, name="user_groups_home_page"),

    # Group management URLs
    path('groups/create/', views.create_group, name='create_group'),
    path('view/<int:group_id>/', views.group_page, name='group_page'),
    path('join/<int:group_id>/', views.join_group, name='join_group'),
    path('leave/<int:group_id>/', views.leave_group, name='leave_group'),
    path('delete/<int:group_id>/', views.delete_group, name='delete_group'),

    # Member management within a group
    path('remove_member/<int:group_id>/<int:user_id>/', views.remove_member, name='remove_member'),

    # Handling join requests for private groups
    path('request_join/<int:group_id>/', views.request_join_group, name='request_join_group'),
    path('view_requests/<int:group_id>/', views.view_join_requests, name='view_join_requests'),
    path('accept_request/<int:group_id>/<int:user_id>/', views.accept_join_request, name='accept_join_request'),
    path('reject_request/<int:group_id>/<int:user_id>/', views.reject_join_request, name='reject_join_request'),

    # Additional URLs for group searching or other functionalities
    path('search/', views.search_groups, name='search_groups'),
]
