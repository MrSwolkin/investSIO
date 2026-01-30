"""
Pytest configuration and shared fixtures for InvestSIO tests.
"""
from datetime import date, timedelta
from decimal import Decimal
import pytest

from brokers.models import Broker, Currency
from categories.models import Category
from tickers.models import Ticker
from inflows.models import Inflow
from outflows.models import Outflow
from dividends.models import Dividend


# ============================================================================
# Currency Fixtures
# ============================================================================

@pytest.fixture
def currency_brl(db):
    """Create BRL currency."""
    return Currency.objects.create(code="BRL", name="Real Brasileiro")


@pytest.fixture
def currency_usd(db):
    """Create USD currency."""
    return Currency.objects.create(code="USD", name="Dolar Americano", exchange_rate=Decimal("5.50"))


# ============================================================================
# Category Fixtures
# ============================================================================

@pytest.fixture
def category_fii(db):
    """Create FII category."""
    return Category.objects.create(title="FII", description="Fundos Imobiliarios")


@pytest.fixture
def category_acao(db):
    """Create Acao category."""
    return Category.objects.create(title="Acao", description="Acoes Brasileiras")


@pytest.fixture
def category_stock(db):
    """Create Stock category."""
    return Category.objects.create(title="Stock", description="Acoes Americanas")


@pytest.fixture
def category_etf(db):
    """Create ETF category."""
    return Category.objects.create(title="ETF", description="Exchange Traded Funds")


# ============================================================================
# Broker Fixtures
# ============================================================================

@pytest.fixture
def broker_xp(db, currency_brl):
    """Create XP broker."""
    return Broker.objects.create(
        name="XP Investimentos",
        currency=currency_brl,
        country="BR",
    )


@pytest.fixture
def broker_inter(db, currency_brl):
    """Create Inter broker."""
    return Broker.objects.create(
        name="Banco Inter",
        currency=currency_brl,
        country="BR",
    )


# ============================================================================
# Ticker Fixtures
# ============================================================================

@pytest.fixture
def ticker_fii(db, category_fii, currency_brl):
    """Create a FII ticker."""
    return Ticker.objects.create(
        name="HGLG11",
        category=category_fii,
        currency=currency_brl,
        sector="Logistica",
    )


@pytest.fixture
def ticker_acao(db, category_acao, currency_brl):
    """Create an Acao ticker."""
    return Ticker.objects.create(
        name="PETR4",
        category=category_acao,
        currency=currency_brl,
        sector="Petroleo",
    )


@pytest.fixture
def ticker_stock(db, category_stock, currency_usd):
    """Create a Stock ticker."""
    return Ticker.objects.create(
        name="AAPL",
        category=category_stock,
        currency=currency_usd,
        sector="Tecnologia",
    )


# ============================================================================
# Inflow Fixtures
# ============================================================================

@pytest.fixture
def inflow_fii(db, ticker_fii, broker_xp):
    """Create an inflow for FII ticker."""
    return Inflow.objects.create(
        ticker=ticker_fii,
        broker=broker_xp,
        cost_price=Decimal("150.00"),
        quantity=10,
        date=date.today() - timedelta(days=30),
    )


@pytest.fixture
def inflow_acao(db, ticker_acao, broker_xp):
    """Create an inflow for Acao ticker."""
    return Inflow.objects.create(
        ticker=ticker_acao,
        broker=broker_xp,
        cost_price=Decimal("35.00"),
        quantity=100,
        date=date.today() - timedelta(days=60),
    )


# ============================================================================
# Outflow Fixtures
# ============================================================================

@pytest.fixture
def outflow_fii(db, ticker_fii, broker_xp, inflow_fii):
    """Create an outflow for FII ticker (requires inflow first)."""
    return Outflow.objects.create(
        ticker=ticker_fii,
        broker=broker_xp,
        cost_price=Decimal("155.00"),
        quantity=5,
        date=date.today() - timedelta(days=10),
    )


# ============================================================================
# Dividend Fixtures
# ============================================================================

@pytest.fixture
def dividend_fii(db, ticker_fii, inflow_fii):
    """Create a dividend for FII ticker (requires inflow first)."""
    return Dividend.objects.create(
        ticker=ticker_fii,
        value=Decimal("0.8500000000"),
        date=date.today() - timedelta(days=15),
        currency="BRL",
        income_type="D",
    )


# ============================================================================
# Date Fixtures
# ============================================================================

@pytest.fixture
def today():
    """Return today's date."""
    return date.today()


@pytest.fixture
def yesterday():
    """Return yesterday's date."""
    return date.today() - timedelta(days=1)


@pytest.fixture
def tomorrow():
    """Return tomorrow's date."""
    return date.today() + timedelta(days=1)


@pytest.fixture
def one_month_ago():
    """Return the date one month ago."""
    return date.today() - timedelta(days=30)
