from django.http import HttpResponse
from rest_framework import generics
from .models import Cryptocurrency, HistoricalPrice
from .serializers import CryptocurrencySerializer, CryptocurrencyHistoricalPriceSerializer, DailyReturnSerializer, RSISerializer
from rest_framework.response import Response
import numpy as np
import logging

class CryptocurrencyListView(generics.ListAPIView):
   queryset = Cryptocurrency.objects.all()
   serializer_class = CryptocurrencySerializer

class CryptocurrencyDetailView(generics.RetrieveAPIView):
   queryset = Cryptocurrency.objects.all()
   serializer_class = CryptocurrencySerializer

class CryptocurrencyDetailByNameView(generics.RetrieveAPIView):
   serializer_class = CryptocurrencySerializer
   lookup_field = 'name'

   def get_queryset(self):
      name = self.kwargs['name']
      return Cryptocurrency.objects.filter(name=name)   

class HistoricalPriceListView(generics.ListAPIView):
   serializer_class = CryptocurrencyHistoricalPriceSerializer
   
   def get_queryset(self):
      name = self.kwargs['name']
      return HistoricalPrice.objects.filter(cryptocurrency__name=name)

class HistoricalPriceRangeView(generics.ListAPIView):
   serializer_class = CryptocurrencyHistoricalPriceSerializer

   def get_queryset(self):
      name = self.request.query_params.get('name')
      from_date = self.request.query_params.get('from_date')
      to_date = self.request.query_params.get('to_date')
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
      serializer = self.get_serializer(data, many=True)
      return Response(serializer.data)

class RSIView(generics.ListAPIView):
   serializer_class = RSISerializer
   
   def get_queryset(self):
      name = self.request.query_params.get('name')
      from_date = self.request.query_params.get('from_date')
      to_date = self.request.query_params.get('to_date')
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
      serializer = self.get_serializer(data, many=True)
      return Response(serializer.data)

logger = logging.getLogger(__name__)

def my_view(request):
   logger.debug('This is a debug message')
   logger.info('This is an info message')
   logger.warning('This is a warning message')
   logger.error('This is an error message')
   logger.critical('This is a critical message')
   return HttpResponse('Logging test')   