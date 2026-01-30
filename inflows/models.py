from django.db import models
from brokers.models import Broker
from tickers.models import Ticker


class Inflow(models.Model):
    TYPE_CHOICES = [
        ("Compra", "Compra"),
        ("Subscrição", "Subscrição")
    ]

    broker = models.ForeignKey(
        Broker,
        on_delete=models.PROTECT,
        related_name="inflows",
        null=True,
        blank=True,
        db_index=True
    )
    ticker = models.ForeignKey(
        Ticker,
        on_delete=models.PROTECT,
        related_name="inflows",
        db_index=True
    )
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(db_index=True)
    tax = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="Compra")

    def save(self, *args, **kwargs):
        if self.quantity and self.cost_price:
            self.total_price = self.cost_price * self.quantity
        else:
            self.total_price = 0
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=['ticker', 'date'], name='inflow_ticker_date_idx'),
            models.Index(fields=['broker', 'date'], name='inflow_broker_date_idx'),
            models.Index(fields=['ticker', 'broker'], name='inflow_ticker_broker_idx'),
        ]

    def __str__(self):
        return f"Compra de {self.ticker} - {self.quantity}"

    @property
    def transaction_type(self):
        return "Compra" if self.type == "Compra" else "Subscrição"
