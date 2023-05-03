"""MusicHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('handle/', views.handle, name='handle'),
    path('handleRegistration/', views.handleRegistration, name='handleRegistration'),
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('home/', views.home, name='home'),
    path('personalCenter/', views.personalCenter, name='personalCenter'),
    path('handleLogin/', views.handleLogin, name='handleLogin'),
    path('userInformation/', views.userInformation, name='userInformation'),
    path('userInformation_normalUser/', views.userInformation_normalUser, name='userInformation_normalUser'),
    path('deleteUser/', views.deleteUser, name="deleteUser"),
    path('addAnyUser/', views.addAnyUser, name="addAnyUser"),
    path('dataAnalysis/', views.dataAnalysis, name="dataAnalysis")
]
