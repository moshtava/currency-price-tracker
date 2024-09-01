from django.db import models

class Cryptocurrency(models.Model):
   name = models.CharField(max_length=100)
   symbol = models.CharField(max_length=10)
   market_cap = models.BigIntegerField()
   price = models.DecimalField(max_digits=20, decimal_places=10)
   
   class Meta:
      unique = ('name')
      indexes = [models.Index(fields=['name']),]

class HistoricalPrice(models.Model):
   cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='historical_prices')
   date = models.DateField()
   price = models.DecimalField(max_digits=20, decimal_places=10)
   
   class Meta:
      unique_together = ('cryptocurrency', 'date')
      indexes = [
      models.Index(fields=['cryptocurrency', 'date']),
      ]