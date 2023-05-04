from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='login'),
    path('handleLogin/', views.handleLogin, name='handleLogin'),

]
