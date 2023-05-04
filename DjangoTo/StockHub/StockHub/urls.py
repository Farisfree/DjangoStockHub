from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('', views.login),
    path('search/', views.search),
    path('register/',views.register),
    path('delete/', views.delete),

]
