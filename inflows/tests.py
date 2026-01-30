"""
Tests for Inflow model validators.
"""
from datetime import date, timedelta
from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError

from brokers.models import Broker, Currency
from categories.models import Category
from tickers.models import Ticker
from inflows.models import Inflow


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


class TestInflowValidators:
    """Tests for Inflow model field validators."""

    def test_valid_inflow(self, ticker, broker):
        """Test creating a valid inflow."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
        )
        inflow.full_clean()
        inflow.save()
        assert inflow.pk is not None
        assert inflow.total_price == Decimal("1000.00")

    def test_quantity_must_be_positive(self, ticker, broker):
        """Test that quantity must be at least 1."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=0,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            inflow.full_clean()
        assert "quantity" in exc_info.value.message_dict

    def test_quantity_negative_raises_error(self, ticker, broker):
        """Test that negative quantity raises validation error."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=-5,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            inflow.full_clean()
        assert "quantity" in exc_info.value.message_dict

    def test_cost_price_must_be_positive(self, ticker, broker):
        """Test that cost_price must be greater than zero."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("0.00"),
            quantity=100,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            inflow.full_clean()
        assert "cost_price" in exc_info.value.message_dict

    def test_cost_price_negative_raises_error(self, ticker, broker):
        """Test that negative cost_price raises validation error."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("-10.00"),
            quantity=100,
            date=date.today(),
        )
        with pytest.raises(ValidationError) as exc_info:
            inflow.full_clean()
        assert "cost_price" in exc_info.value.message_dict

    def test_tax_cannot_be_negative(self, ticker, broker):
        """Test that tax cannot be negative."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
            tax=Decimal("-1.00"),
        )
        with pytest.raises(ValidationError) as exc_info:
            inflow.full_clean()
        assert "tax" in exc_info.value.message_dict

    def test_tax_zero_is_valid(self, ticker, broker):
        """Test that zero tax is valid."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
            tax=Decimal("0.00"),
        )
        inflow.full_clean()
        inflow.save()
        assert inflow.pk is not None

    def test_future_date_raises_error(self, ticker, broker):
        """Test that future date raises validation error."""
        future_date = date.today() + timedelta(days=1)
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=future_date,
        )
        with pytest.raises(ValidationError) as exc_info:
            inflow.full_clean()
        assert "date" in exc_info.value.message_dict

    def test_today_date_is_valid(self, ticker, broker):
        """Test that today's date is valid."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
        )
        inflow.full_clean()
        inflow.save()
        assert inflow.pk is not None

    def test_past_date_is_valid(self, ticker, broker):
        """Test that past dates are valid."""
        past_date = date.today() - timedelta(days=30)
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=past_date,
        )
        inflow.full_clean()
        inflow.save()
        assert inflow.pk is not None

    def test_total_price_auto_calculated(self, ticker, broker):
        """Test that total_price is auto-calculated on save."""
        inflow = Inflow(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("25.50"),
            quantity=10,
            date=date.today(),
        )
        inflow.full_clean()
        inflow.save()
        assert inflow.total_price == Decimal("255.00")


class TestInflowModel:
    """Tests for Inflow model methods and properties."""

    def test_str_representation(self, ticker, broker):
        """Test the string representation of Inflow."""
        inflow = Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
        )
        assert str(inflow) == f"Compra de {ticker} - 100"

    def test_transaction_type_compra(self, ticker, broker):
        """Test transaction_type property returns Compra."""
        inflow = Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today(),
            type="Compra",
        )
        assert inflow.transaction_type == "Compra"

    def test_transaction_type_subscricao(self, ticker, broker):
        """Test transaction_type property returns Subscricao."""
        inflow = Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=50,
            date=date.today(),
            type="Subscrição",
        )
        assert inflow.transaction_type == "Subscrição"

    def test_inflow_without_broker(self, ticker):
        """Test inflow can be created without broker."""
        inflow = Inflow.objects.create(
            ticker=ticker,
            broker=None,
            cost_price=Decimal("15.00"),
            quantity=20,
            date=date.today(),
        )
        assert inflow.pk is not None
        assert inflow.broker is None

    def test_ordering_by_date_descending(self, ticker, broker):
        """Test inflows are ordered by date descending."""
        inflow1 = Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=10,
            date=date.today() - timedelta(days=30),
        )
        inflow2 = Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=10,
            date=date.today(),
        )
        inflows = list(Inflow.objects.all())
        assert inflows[0] == inflow2
        assert inflows[1] == inflow1
