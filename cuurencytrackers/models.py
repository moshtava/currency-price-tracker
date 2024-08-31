from django.db import models

class Cryptocurrency(models.Model):
   name = models.CharField(max_length=100)
   symbol = models.CharField(max_length=10)
   market_cap = models.BigIntegerField()
   price = models.DecimalField(max_digits=20, decimal_places=10)

