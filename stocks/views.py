import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Trade
from .serializers import TradeSerializer

API_KEY = '24C1F795-41A0-4DD5-88A8-273B4DB96B65'
API_URL = 'https://rest.coinapi.io/v1/trades/latest?symbol=BITSTAMP_SPOT_BTC_USD'
HEADERS = {'X-CoinAPI-Key': API_KEY}

@api_view(['GET'])
def fetch_trades(request):
    response = requests.get(API_URL, headers=HEADERS)
    
    if response.status_code == 200:
        Trade.objects.all().delete()
        trades = response.json()
        for trade_data in trades:
            trade = Trade(
                symbol=trade_data['symbol_id'],
                price=trade_data['price'],
                size=trade_data['size'],
                taker_side=trade_data['taker_side'],
                timestamp=trade_data['time_exchange']
            )
            trade.save()
        return Response({'message': 'Trades fetched and saved successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Failed to fetch data from CoinAPI'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_trades(request):
    trades = Trade.objects.all()
    serializer = TradeSerializer(trades, many=True)
    return Response(serializer.data)

