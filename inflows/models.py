from django.db import models


from django.db import models
from brokers.models import Broker
from tickers.models import Ticker


class Inflow(models.Model):
    broker = models.ForeignKey(
        Broker, on_delete=models.PROTECT, related_name="inflows")
    ticker = models.ForeignKey(
        Ticker, on_delete=models.PROTECT, related_name="inflows")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    tax = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.quantity and self.cost_price:
            self.total_price = self.cost_price * self.quantity
        else:
            self.total_price = 0
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Compra de {self.ticker} - {self.quantity}"

    @property
    def transaction_type(self):
        return "Compra"
