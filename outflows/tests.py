"""
Tests for Outflow model validators.
"""
from datetime import date, timedelta
from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError

from brokers.models import Broker, Currency
from categories.models import Category
from tickers.models import Ticker
from outflows.models import Outflow


@pytest.fixture
def currency(db):
    """Create a test currency."""
    return Currency.objects.create(code="BRL", name="Real")


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(title="FII", description="Fundos Imobiliarios")


@pytest.fixture
def broker(db, currency):
    """Create a test broker."""
    return Broker.objects.create(name="Test Broker", currency=currency)


@pytest.fixture
def ticker(db, category, currency):
    """Create a test ticker."""
    return Ticker.objects.create(
        name="TEST11",
        category=category,
        currency=currency,
    )


class TestOutflowValidators:
    """Tests for Outflow model field validators."""

    def test_valid_outflow(self, ticker, broker):
        """Test creating a valid outflow."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("15.00"),
            quantity=50,
            date=date.today(),
        )
        outflow.full_clean()
        outflow.save()
        assert outflow.pk is not None
        assert outflow.total_price == Decimal("750.00")

    def test_quantity_must_be_positive(self, ticker, broker):
        """Test that quantity must be at least 1."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=0,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            outflow.full_clean()
        assert "quantity" in exc_info.value.message_dict

    def test_quantity_negative_raises_error(self, ticker, broker):
        """Test that negative quantity raises validation error."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=-5,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            outflow.full_clean()
        assert "quantity" in exc_info.value.message_dict

    def test_cost_price_must_be_positive(self, ticker, broker):
        """Test that cost_price must be greater than zero."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("0.00"),
            quantity=100,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            outflow.full_clean()
        assert "cost_price" in exc_info.value.message_dict

    def test_cost_price_negative_raises_error(self, ticker, broker):
        """Test that negative cost_price raises validation error."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("-10.00"),
            quantity=100,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            outflow.full_clean()
        assert "cost_price" in exc_info.value.message_dict

    def test_tax_cannot_be_negative(self, ticker, broker):
        """Test that tax cannot be negative."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
            tax=Decimal("-1.00"),
        )
        with pytest.raises(ValidationError) as exc_info:
            outflow.full_clean()
        assert "tax" in exc_info.value.message_dict

    def test_tax_zero_is_valid(self, ticker, broker):
        """Test that zero tax is valid."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
            tax=Decimal("0.00"),
        )
        outflow.full_clean()
        outflow.save()
        assert outflow.pk is not None

    def test_future_date_raises_error(self, ticker, broker):
        """Test that future date raises validation error."""
        future_date = date.today() + timedelta(days=1)
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=future_date,
        )
        with pytest.raises(ValidationError) as exc_info:
            outflow.full_clean()
        assert "date" in exc_info.value.message_dict

    def test_today_date_is_valid(self, ticker, broker):
        """Test that today's date is valid."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
        )
        outflow.full_clean()
        outflow.save()
        assert outflow.pk is not None

    def test_past_date_is_valid(self, ticker, broker):
        """Test that past dates are valid."""
        past_date = date.today() - timedelta(days=30)
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=past_date,
        )
        outflow.full_clean()
        outflow.save()
        assert outflow.pk is not None

    def test_total_price_auto_calculated(self, ticker, broker):
        """Test that total_price is auto-calculated on save."""
        outflow = Outflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("30.00"),
            quantity=20,
            date=date.today(),
        )
        outflow.full_clean()
        outflow.save()
        assert outflow.total_price == Decimal("600.00")


class TestOutflowModel:
    """Tests for Outflow model methods and properties."""

    def test_str_representation(self, ticker, broker):
        """Test the string representation of Outflow."""
        outflow = Outflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=50,
            date=date.today(),
        )
        assert str(outflow) == f"Compra de {ticker} - 50"

    def test_transaction_type_is_venda(self, ticker, broker):
        """Test transaction_type property always returns Venda."""
        outflow = Outflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=25,
            date=date.today(),
        )
        assert outflow.transaction_type == "Venda"

    def test_outflow_without_broker(self, ticker):
        """Test outflow can be created without broker."""
        outflow = Outflow.objects.create(
            ticker=ticker,
            broker=None,
            cost_price=Decimal("15.00"),
            quantity=20,
            date=date.today(),
        )
        assert outflow.pk is not None
        assert outflow.broker is None

    def test_ordering_by_date_descending(self, ticker, broker):
        """Test outflows are ordered by date descending."""
        outflow1 = Outflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=10,
            date=date.today() - timedelta(days=30),
        )
        outflow2 = Outflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=10,
            date=date.today(),
        )
        outflows = list(Outflow.objects.all())
        assert outflows[0] == outflow2
        assert outflows[1] == outflow1
