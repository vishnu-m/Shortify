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
from django.contrib.auth.views import (
     login, logout, password_reset , password_reset_done, password_reset_confirm,
     password_reset_complete )
from django.urls import path 
from django.conf.urls import url
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf.urls import url, include

from kutt import settings
from shortify import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('short/',views.short),
    path('signup/',views.signup),
    path('validate/',views.validate),
    path('login/',views.login_page, name = 'login'),
    path('logout/',logout, name = 'logout' ),
    path('editprofile/' , views.EditProfile),
    path('verify/', views.verify),
    path('custom_shorten/',views.custom_shorten),
    path('statistics/', views.statistics),
    path('get_statistics/', views.show_stati),
    path('profile/',views.profile),
    path("password-reset/" , password_reset ,{'template_name':'reset-password.html'} , name = 'reset-password'),
    path("password-reset/done/" , password_reset_done ,{'template_name':'password_reset_done.html'} , name = 'password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$' ,
     password_reset_confirm ,{'template_name':'password_reset_confirm.html'}, name = 'password_reset_confirm'),

    path('reset-password/complete', password_reset_complete ,{'template_name':'password_reset_complete.html'} ,name = 'password_reset_complete'),

    url(r'^auth/', include('social_django.urls', namespace='social')),


    # keep this section in the bottom in order to prevent overriding the shortened URL and pre defined URL
    re_path(r'^.*/$',views.get_url),    # shortened url matching
] 



urlpatterns += staticfiles_urlpatterns()