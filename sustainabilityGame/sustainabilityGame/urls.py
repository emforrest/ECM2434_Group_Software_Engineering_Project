"""
URL configuration for sustainabilityGame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

Authors:
- Eleanor Forrest
"""
from django.contrib import admin
from django.urls import include, path
from login import views

urlpatterns = [
    path("", include("main.urls")),
    path("register/", include("register.urls")),
    path('accounts/login/', views.login_view),
    path('logout/', views.logout_view),
    path("login/", include("login.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path("user/", include("user.urls")),
    path("groups/", include("groups.urls")),
    path("admin/", admin.site.urls),
    path("adminUser/", include("adminUser.urls"))
]