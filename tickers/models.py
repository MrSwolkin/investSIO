from django.db import models
from django.core.exceptions import ValidationError
from categories.models import Category
from brokers.models import Currency




class Ticker(models.Model):
    name = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="tickers")
    quantity = models.IntegerField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="tickers")
    sector = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    
    @property
    def total_quantity(self):
        from app import metrics
        metrics = metrics.get_ticker_metrics(self)
        return metrics["total_quantity"]
