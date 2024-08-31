from rest_framework import serializers
from .models import Cryptocurrency, HistoricalPrice

class CryptocurrencySerializer(serializers.ModelSerializer):
   class Meta:
      model = Cryptocurrency
      fields = '__all__'

