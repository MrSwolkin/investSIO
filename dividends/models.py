from django.db import models
from tickers.models import Ticker
# Create your models here.

class Dividend(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.PROTECT, related_name="dividens")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    quantity_quote = models.IntegerField()
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ["-date"]
    
    def __str__(self):
        return f"Dividendo {self.ticker.name} - {self.total_value}"
    

class DeclaredDividend(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.PROTECT, related_name="declared_dividens")
    value_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    
    class Meta:
        ordering = ["-payment_date"]
        
    def __str__(self):
        return f"Dividendo anunciado de {self.ticker.name}"