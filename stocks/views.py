import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Trade
from .serializers import TradeSerializer

API_KEY = '24C1F795-41A0-4DD5-88A8-273B4DB96B65'
API_URL = 'https://rest.coinapi.io/v1/trades/latest?symbol=BITSTAMP_SPOT_BTC_USD'
HEADERS = {'X-CoinAPI-Key': API_KEY}

# Global variable to temporarily hold fetched data
temp_trades = []

@api_view(['GET'])
def fetch_trades(request):
    global temp_trades
    response = requests.get(API_URL, headers=HEADERS)
    
    if response.status_code == 200:
        trades = response.json()
        temp_trades = []

        for trade_data in trades:
            temp_trades.append({
                'symbol': trade_data['symbol_id'],
                'price': trade_data['price'],
                'size': trade_data['size'],
                'taker_side': trade_data['taker_side'],
                'timestamp': trade_data['time_exchange']
            })

        return Response({'message': 'Trades fetched successfully.', 'data': temp_trades}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Failed to fetch data from CoinAPI'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def save_trades(request):
    global temp_trades

    user_response = request.data.get('response')
    if user_response is None:
        return Response({"error": "User response not provided"}, status=status.HTTP_400_BAD_REQUEST)

    if user_response.lower() == 'yes':
        try:
            Trade.objects.all().delete()
            for trade_data in temp_trades:
                trade = Trade(
                    symbol=trade_data['symbol'],
                    price=trade_data['price'],
                    size=trade_data['size'],
                    taker_side=trade_data['taker_side'],
                    timestamp=trade_data['timestamp']
                )
                trade.save()

            temp_trades = []
            return Response({"message": "Trades saved successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to save trades: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif user_response.lower() == 'no':
        temp_trades = []
        return Response({"message": "Trades discarded"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid user response"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_trades(request):
    trades = Trade.objects.all()
    serializer = TradeSerializer(trades, many=True)
    return Response(serializer.data)
