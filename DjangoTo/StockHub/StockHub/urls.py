from django.urls import path
from . import views

urlpatterns = [
    #path('login/', views.login),
    path('login/', views.login),
    # path('search/', views.search),
    path('register/',views.register),
    path('delete/', views.delete),
    path('home/',views.home),
    # path('searchlist/', views.search_list),
    path('', views.search_list),

    path('stock_basic_info/', views.stock_basic_info),
    path('stock_daily_data/', views.stock_daily_data),
    path('stock_dividend_data/',views.stock_dividend_data),
    path('stock_fees_data/', views.stock_fees_data),
    path('stock_financial_data/', views.stock_financial_data),
    path('stock_price_data/', views.stock_price_data),
    path('stock_ratios_data/', views.stock_ratios_data),
    path('stock_return_data/', views.stock_return_data),
    path('stock_shares_data/', views.stock_shares_data),

    path('test/', views.test),

]
