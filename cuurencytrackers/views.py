from rest_framework import generics
from .models import Cryptocurrency, HistoricalPrice
from .serializers import CryptocurrencySerializer, CryptocurrencyHistoricalPriceSerializer

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
