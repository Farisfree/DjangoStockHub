from django.urls import path
from . import views

urlpatterns = [

    path('', views.login),
    path('login/', views.login),
    path('register/',views.register),
    path('delete/', views.delete),
    path('home/',views.home),
    path('search_list/', views.search_list),
    path('stock_basic_info/', views.stock_basic_info),
    path('stock_daily_data/', views.stock_daily_data),
    path('stock_dividend_data/',views.stock_dividend_data),
    path('stock_fees_data/', views.stock_fees_data),
    path('stock_financial_data/', views.stock_financial_data),
    path('stock_price_data/', views.stock_price_data),
    path('stock_ratios_data/', views.stock_ratios_data),
    path('stock_return_data/', views.stock_return_data),
    path('stock_shares_data/', views.stock_shares_data),

    path('collect/', views.collect),
    path('collectInterface/', views.collectInterface),
    path('historyShow/', views.historyShow),

]
