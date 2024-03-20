"""
URL configuration for carbonCommuter project.

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
- Sam Townley
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from login import views as login_views
from carbonCommuter import views
from django.conf.urls import handler404, handler500, handler403, handler400


urlpatterns = [
    path("", include("main.urls")),
    path("register/", include("register.urls")),
    path('accounts/login/', login_views.login_view),
    path('logout/', login_views.logout_view),
    path("login/", include("login.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path("user/", include("user.urls")),
    path("groups/", include("groups.urls")),
    path("dev/", admin.site.urls),
    path("admin/", include("adminUser.urls")),
]


if settings.DEBUG:
    # handling media in Debug mode (images, gifs, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    handler400 = views.error_400
    handler403 = views.error_403
    handler404 = views.error_404
    handler500 = views.error_500