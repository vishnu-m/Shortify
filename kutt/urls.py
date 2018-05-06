"""kutt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.conf.urls.static import static
from kutt import settings
from shortify import views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('short/',views.short),
    path('signup/',views.signup),
    path('validate/',views.validate),
    path('login/',views.login_user),
    path('logout/',views.logout_user),
    path('verify/', views.verify),
    path('custom_shorten/',views.custom_shorten),
    re_path(r'^reset-password/$', password_reset, name='reset_password'),
    re_path(r'^reset-password/done/$', password_reset_done, name='password_reset_done'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,name='password_reset_confirm'),
    re_path(r'^.*/$',views.get_url),    # shortened url matching
] 



urlpatterns += staticfiles_urlpatterns()