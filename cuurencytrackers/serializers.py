from rest_framework import serializers
from .models import Cryptocurrency, HistoricalPrice

class CryptocurrencySerializer(serializers.ModelSerializer):
   class Meta:
      model = Cryptocurrency
      fields = '__all__'

class HistoricalPriceSerializer(serializers.ModelSerializer):
   class Meta:
      model = HistoricalPrice
      fields = '__all__'

