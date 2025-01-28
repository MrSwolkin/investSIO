from django.db import models
from categories.models import Category
from brokers.models import Currency


class Ticker(models.Model):
    name = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="tickers")
    quantity = models.IntegerField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="tickres")
    sector = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name