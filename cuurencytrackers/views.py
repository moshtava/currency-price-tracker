from django.http import HttpResponse
from rest_framework import generics
from .models import Cryptocurrency, HistoricalPrice
from .serializers import CryptocurrencySerializer, CryptocurrencyHistoricalPriceSerializer, DailyReturnSerializer, RSISerializer
from rest_framework.response import Response
import numpy as np
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from .models import Cryptocurrency, HistoricalPrice
from .serializers import CryptocurrencySerializer, HistoricalPriceSerializer

class GenerateDataView(APIView):
   def get(self, request):
      date_range = pd.date_range(start='2023-01-01', end='2024-02-02')
      cryptocurrencies = [
      {'name': 'Bitcoin', 'symbol': 'BTC', 'market_cap': 600000000000, 'price': 50000},
      {'name': 'Ethereum', 'symbol': 'ETH', 'market_cap': 250000000000, 'price': 4000},
      {'name': 'Ripple', 'symbol': 'XRP', 'market_cap': 50000000000, 'price': 1}
      ]
      historical_data = []
      for crypto in cryptocurrencies:
         for date in date_range:
            price = np.random.uniform(low=crypto['price'] * 0.8, high=crypto['price'] * 1.2)
            historical_data.append({
            'cryptocurrency': crypto['name'],
            'date': date,
            'price': round(price, 10)
            })
      crypto_df = pd.DataFrame(cryptocurrencies)
      historical_df = pd.DataFrame(historical_data)
      crypto_df.to_csv('./sample_cryptocurrencies.csv', index=False)
      historical_df.to_csv('./sample_historical_prices.csv', index=False)
      return Response({"message": "Sample data generated and saved to 'sample_cryptocurrencies.csv' and 'sample_historical_prices.csv'."})

class InsertDataView(APIView):
   def get(self, request):
      crypto_csv_path = './sample_cryptocurrencies.csv'
      historical_csv_path = './sample_historical_prices.csv'
      crypto_data = pd.read_csv(crypto_csv_path)
      historical_data = pd.read_csv(historical_csv_path)
      for _, row in crypto_data.iterrows():
         crypto, created = Cryptocurrency.objects.get_or_create(
         name=row['name'],
         symbol=row['symbol'],
         defaults={'market_cap': row['market_cap'], 'price': row['price']}
         )
      for _, row in historical_data.iterrows():
         crypto = Cryptocurrency.objects.get(name=row['cryptocurrency'])
         HistoricalPrice.objects.create(
         cryptocurrency=crypto,
         date=row['date'],
         price=row['price']
         )
      return Response({"message": "Data ingestion completed successfully."})
   
logger = logging.getLogger(__name__)

class CryptocurrencyListView(generics.ListAPIView):
   serializer_class = CryptocurrencySerializer

   def get_queryset(self):
      logger.info("Listing the first 10 cryptocurrencies")
      return Cryptocurrency.objects.all()[:10]
   
   def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

class CryptocurrencyDetailView(generics.RetrieveAPIView):
   queryset = Cryptocurrency.objects.all()
   serializer_class = CryptocurrencySerializer
   
   def retrieve(self, request, *args, **kwargs):
      logger.info(f"Retrieving details for cryptocurrency ID: {kwargs['pk']}")
      return super().retrieve(request, *args, **kwargs)

class CryptocurrencyDetailByNameView(generics.RetrieveAPIView):
   serializer_class = CryptocurrencySerializer
   lookup_field = 'name'
   
   def get_queryset(self):
      name = self.kwargs['name']
      logger.info(f"Retrieving details for cryptocurrency name: {name}")
      return Cryptocurrency.objects.filter(name=name)
   
class HistoricalPriceListView(generics.ListAPIView):
   serializer_class = CryptocurrencyHistoricalPriceSerializer
   
   def get_queryset(self):
      name = self.kwargs['name']
      logger.info(f"Listing historical prices for cryptocurrency name: {name}")
      return HistoricalPrice.objects.filter(cryptocurrency__name=name)

class HistoricalPriceRangeView(generics.ListAPIView):
   serializer_class = CryptocurrencyHistoricalPriceSerializer
   
   def get_queryset(self):
      name = self.request.query_params.get('name')
      from_date = self.request.query_params.get('from_date')
      to_date = self.request.query_params.get('to_date')
      logger.info(f"Listing historical prices for cryptocurrency name: {name} from {from_date} to {to_date}")
      return HistoricalPrice.objects.filter(
      cryptocurrency__name=name,
      date__range=[from_date, to_date]
      )
   
class DailyReturnView(generics.ListAPIView):
   serializer_class = DailyReturnSerializer
   
   def get_queryset(self):
      name = self.request.query_params.get('name')
      from_date = self.request.query_params.get('from_date')
      to_date = self.request.query_params.get('to_date')
      logger.info(f"Calculating daily returns for cryptocurrency name: {name} from {from_date} to {to_date}")
      return HistoricalPrice.objects.filter(
      cryptocurrency__name=name,
      date__range=[from_date, to_date]
      ).order_by('date')
   
   def list(self, request, *args, **kwargs):
      queryset = self.get_queryset()
      data = []
      for i in range(1, len(queryset)):
         today = queryset[i]
         yesterday = queryset[i-1]
         daily_return = (today.price - yesterday.price) / yesterday.price
         data.append({
         'date': today.date,
         'daily_return': daily_return
         })
      logger.debug(f"Daily returns data: {data}")
      serializer = self.get_serializer(data, many=True)
      return Response(serializer.data)

class RSIView(generics.ListAPIView):
   serializer_class = RSISerializer
   
   def get_queryset(self):
      name = self.request.query_params.get('name')
      from_date = self.request.query_params.get('from_date')
      to_date = self.request.query_params.get('to_date')
      logger.info(f"Calculating RSI for cryptocurrency name: {name} from {from_date} to {to_date}")
      return HistoricalPrice.objects.filter(
      cryptocurrency__name=name,
      date__range=[from_date, to_date]
      ).order_by('date')
   
   def list(self, request, *args, **kwargs):
      period = int(request.query_params.get('period', 14))
      queryset = self.get_queryset()
      prices = np.array([item.price for item in queryset])
      deltas = np.diff(prices)
      seed = deltas[:period+1]
      up = seed[seed >= 0].sum() / period
      down = -seed[seed < 0].sum() / period
      rs = up / down
      rsi = np.zeros_like(prices)
      rsi[:period] = 100. - 100. / (1. + rs)
      for i in range(period, len(prices)):
         delta = deltas[i - 1]
      if delta > 0:
         upval = delta
         downval = 0.
      else:
         upval = 0.
         downval = -delta
      up = (up * (period - 1) + upval) / period
      down = (down * (period - 1) + downval) / period
      rs = up / down
      rsi[i] = 100. - 100. / (1. + rs)
      data = [{'date': queryset[i].date, 'rsi': rsi[i]} for i in range(len(rsi))]
      logger.debug(f"RSI data: {data}")
      serializer = self.get_serializer(data, many=True)
      return Response(serializer.data)
   