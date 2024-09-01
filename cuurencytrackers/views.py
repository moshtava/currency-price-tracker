from rest_framework import generics
from .models import Cryptocurrency
from .serializers import CryptocurrencySerializer

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