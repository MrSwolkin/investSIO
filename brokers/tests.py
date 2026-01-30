"""
Tests for Broker and Currency models.
"""
import pytest

from brokers.models import Broker, Currency


class TestCurrencyModel:
    """Tests for Currency model."""

    def test_create_currency(self, db):
        """Test creating a currency."""
        currency = Currency.objects.create(code="BRL", name="Real Brasileiro")
        assert currency.pk is not None
        assert currency.code == "BRL"
        assert currency.name == "Real Brasileiro"

    def test_currency_str(self, db):
        """Test currency string representation."""
        currency = Currency.objects.create(code="USD", name="Dolar Americano")
        assert str(currency) == "USD"

    def test_currency_ordering(self, db):
        """Test currencies are ordered by code."""
        Currency.objects.create(code="USD", name="Dolar")
        Currency.objects.create(code="BRL", name="Real")
        Currency.objects.create(code="EUR", name="Euro")
        currencies = list(Currency.objects.all())
        assert currencies[0].code == "BRL"
        assert currencies[1].code == "EUR"
        assert currencies[2].code == "USD"


class TestBrokerModel:
    """Tests for Broker model."""

    def test_create_broker(self, db):
        """Test creating a broker."""
        currency = Currency.objects.create(code="BRL", name="Real")
        broker = Broker.objects.create(
            name="XP Investimentos",
            currency=currency,
            country="BR",
        )
        assert broker.pk is not None
        assert broker.name == "XP Investimentos"
        assert broker.country == "BR"

    def test_broker_str(self, db):
        """Test broker string representation."""
        broker = Broker.objects.create(name="Nu Invest")
        assert str(broker) == "Nu Invest"

    def test_broker_without_currency(self, db):
        """Test broker can be created without currency."""
        broker = Broker.objects.create(name="Test Broker")
        assert broker.pk is not None
        assert broker.currency is None

    def test_broker_with_optional_fields(self, db):
        """Test broker with all optional fields."""
        currency = Currency.objects.create(code="BRL", name="Real")
        broker = Broker.objects.create(
            name="Complete Broker",
            account_number="12345-6",
            country="BR",
            currency=currency,
            description="Test description",
        )
        assert broker.account_number == "12345-6"
        assert broker.description == "Test description"
