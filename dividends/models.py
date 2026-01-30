from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from tickers.models import Ticker
from inflows.models import Inflow


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

    ticker = models.ForeignKey(
        Ticker,
        on_delete=models.PROTECT,
        related_name="dividends",
        db_index=True
    )
    value = models.DecimalField(
        max_digits=12,
        decimal_places=10,
        validators=[MinValueValidator(0, message="O valor nao pode ser negativo.")]
    )
    date = models.DateField(db_index=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="BRL")
    quantity_quote = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="A quantidade nao pode ser negativa.")]
    )
    total_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    income_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="D")

    def clean(self):
        """Valida os dados antes de salvar."""
        super().clean()
        if self.date and self.date > timezone.now().date():
            raise ValidationError({
                'date': 'A data nao pode ser no futuro.'
            })

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
        indexes = [
            models.Index(fields=['ticker', 'date'], name='dividend_ticker_date_idx'),
            models.Index(fields=['date', 'currency'], name='dividend_date_currency_idx'),
        ]

    def __str__(self):
        return f"Dividendo {self.ticker.name} - {self.total_value}"


class DeclaredDividend(models.Model):
    ticker = models.ForeignKey(
        Ticker,
        on_delete=models.PROTECT,
        related_name="declared_dividends",
        db_index=True
    )
    value_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(db_index=True)

    class Meta:
        ordering = ["-payment_date"]
        indexes = [
            models.Index(fields=['ticker', 'payment_date'], name='declared_div_ticker_date_idx'),
        ]

    def __str__(self):
        return f"Dividendo anunciado de {self.ticker.name}"
