from django.urls import path
from .views import fetch_trades, list_trades, save_trades

urlpatterns = [
    path('load', fetch_trades, name='load'),
    path('save', save_trades, name='save_trades'),
    path('get-trades', list_trades, name='get_trades'),
]
