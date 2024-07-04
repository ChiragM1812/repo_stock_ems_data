from django.urls import path
from .views import fetch_trades, list_trades

urlpatterns = [
    path('load', fetch_trades, name='load'),
    path('get-trades', list_trades, name='get_trades'),
]
