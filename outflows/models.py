from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from brokers.models import Broker
from tickers.models import Ticker


class Outflow(models.Model):
    broker = models.ForeignKey(
        Broker,
        on_delete=models.PROTECT,
        related_name="outflows",
        null=True,
        blank=True,
        db_index=True
    )
    ticker = models.ForeignKey(
        Ticker,
        on_delete=models.PROTECT,
        related_name="outflows",
        db_index=True
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="O preco deve ser maior que zero.")]
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1, message="A quantidade deve ser pelo menos 1.")]
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(db_index=True)
    tax = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, message="A taxa nao pode ser negativa.")]
    )

    def clean(self):
        """Valida os dados antes de salvar."""
        super().clean()
        if self.date and self.date > timezone.now().date():
            raise ValidationError({
                'date': 'A data nao pode ser no futuro.'
            })

    def save(self, *args, **kwargs):
        if self.quantity and self.cost_price:
            self.total_price = self.cost_price * self.quantity
        else:
            self.total_price = 0
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=['ticker', 'date'], name='outflow_ticker_date_idx'),
            models.Index(fields=['broker', 'date'], name='outflow_broker_date_idx'),
            models.Index(fields=['ticker', 'broker'], name='outflow_ticker_broker_idx'),
        ]

    def __str__(self):
        return f"Compra de {self.ticker} - {self.quantity}"

    @property
    def transaction_type(self):
        return "Venda"
