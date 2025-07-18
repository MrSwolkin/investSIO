from django.db import models
from tickers.models import Ticker
from inflows.models import Inflow
# Create your models here.

class Dividend(models.Model):
    TYPE_CHOICES = [
        ("D", "Dividendos"),
        ("J", "Juros de Capital Próprio"),
        ("A", "Amortização")
    ]
    CURRENCY_CHOICES = [
        ("BRL", "Real"),
        ("USD", "Dólar"),
    ]

    ticker = models.ForeignKey(Ticker, on_delete=models.PROTECT, related_name="dividens")
    value = models.DecimalField(max_digits=12, decimal_places=10)
    date = models.DateField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="BRL")
    quantity_quote = models.IntegerField(default=0)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    income_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="D")


    def save(self, *args, **kwargs):
        if not self.quantity_quote:
            self.quantity_quote = Inflow.objects.filter(
                ticker=self.ticker,
                date__lte=self.date    
            ).aggregate(total=models.Sum("quantity"))["total"] or 0
            
            self.total_value = float(self.value) * float(self.quantity_quote) if self.value and self.quantity_quote else 0
        super().save(*args, **kwargs)

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