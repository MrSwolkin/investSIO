"""
Tests for Ticker model.
"""
from datetime import date, timedelta
from decimal import Decimal
import pytest

from brokers.models import Broker, Currency
from categories.models import Category
from tickers.models import Ticker
from inflows.models import Inflow
from outflows.models import Outflow


@pytest.fixture
def currency(db):
    """Create a test currency."""
    return Currency.objects.create(code="BRL", name="Real")


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(title="FII", description="Fundos Imobiliarios")


class TestTickerModel:
    """Tests for Ticker model."""

    def test_create_ticker(self, currency, category):
        """Test creating a ticker."""
        ticker = Ticker.objects.create(
            name="HGLG11",
            category=category,
            currency=currency,
        )
        assert ticker.pk is not None
        assert ticker.name == "HGLG11"
        assert ticker.category == category
        assert ticker.currency == currency

    def test_ticker_str(self, currency, category):
        """Test ticker string representation."""
        ticker = Ticker.objects.create(
            name="PETR4",
            category=category,
            currency=currency,
        )
        assert str(ticker) == "PETR4"

    def test_ticker_unique_name(self, currency, category):
        """Test ticker name must be unique."""
        Ticker.objects.create(
            name="VALE3",
            category=category,
            currency=currency,
        )
        with pytest.raises(Exception):
            Ticker.objects.create(
                name="VALE3",
                category=category,
                currency=currency,
            )

    def test_ticker_with_optional_fields(self, currency, category):
        """Test ticker with all optional fields."""
        ticker = Ticker.objects.create(
            name="ITUB4",
            category=category,
            currency=currency,
            sector="Bancario",
            description="Itau Unibanco",
        )
        assert ticker.sector == "Bancario"
        assert ticker.description == "Itau Unibanco"

    def test_ticker_ordering(self, currency, category):
        """Test tickers are ordered by name."""
        Ticker.objects.create(name="VALE3", category=category, currency=currency)
        Ticker.objects.create(name="AAPL", category=category, currency=currency)
        Ticker.objects.create(name="PETR4", category=category, currency=currency)
        tickers = list(Ticker.objects.all())
        assert tickers[0].name == "AAPL"
        assert tickers[1].name == "PETR4"
        assert tickers[2].name == "VALE3"

    def test_ticker_default_quantity(self, currency, category):
        """Test ticker has default quantity of 0."""
        ticker = Ticker.objects.create(
            name="BBDC4",
            category=category,
            currency=currency,
        )
        assert ticker.quantity == 0


@pytest.fixture
def broker(db, currency):
    """Create a test broker."""
    return Broker.objects.create(name="Test Broker", currency=currency)


class TestTickerTotalQuantity:
    """Tests for Ticker total_quantity property."""

    def test_total_quantity_with_no_transactions(self, currency, category):
        """Test total_quantity is 0 when no transactions exist."""
        ticker = Ticker.objects.create(
            name="EMPTY11",
            category=category,
            currency=currency,
        )
        assert ticker.total_quantity == 0

    def test_total_quantity_with_inflows_only(self, currency, category, broker):
        """Test total_quantity with only inflows."""
        ticker = Ticker.objects.create(
            name="INFL11",
            category=category,
            currency=currency,
        )
        Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today() - timedelta(days=30),
        )
        Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("12.00"),
            quantity=50,
            date=date.today(),
        )
        assert ticker.total_quantity == 150

    def test_total_quantity_with_inflows_and_outflows(self, currency, category, broker):
        """Test total_quantity with inflows and outflows."""
        ticker = Ticker.objects.create(
            name="MIX11",
            category=category,
            currency=currency,
        )
        Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("10.00"),
            quantity=100,
            date=date.today() - timedelta(days=60),
        )
        Outflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("12.00"),
            quantity=30,
            date=date.today() - timedelta(days=30),
        )
        Inflow.objects.create(
            ticker=ticker,
            broker=broker,
            cost_price=Decimal("11.00"),
            quantity=20,
            date=date.today(),
        )
        # 100 - 30 + 20 = 90
        assert ticker.total_quantity == 90
