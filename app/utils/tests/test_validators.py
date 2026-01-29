"""
Tests for input validators.
"""

import pytest
from django.http import Http404
from app.utils.validators import (
    validate_ticker_name,
    validate_broker_name,
    validate_category_title,
    validate_positive_integer,
    validate_year,
    validate_month,
    validate_currency_code,
)


class TestValidateTickerName:
    """Tests for validate_ticker_name function."""

    def test_valid_ticker(self):
        """Test valid ticker names are accepted."""
        assert validate_ticker_name("PETR4") == "PETR4"
        assert validate_ticker_name("petr4") == "PETR4"
        assert validate_ticker_name("VALE3") == "VALE3"
        assert validate_ticker_name("BOVA11") == "BOVA11"
        assert validate_ticker_name("AAPL") == "AAPL"

    def test_none_returns_none(self):
        """Test None input returns None."""
        assert validate_ticker_name(None) is None
        assert validate_ticker_name("") is None

    def test_invalid_ticker_raises_404(self):
        """Test invalid ticker names raise Http404."""
        with pytest.raises(Http404):
            validate_ticker_name("PETR4!")  # Special character

        with pytest.raises(Http404):
            validate_ticker_name("DROP TABLE")  # SQL injection attempt

        with pytest.raises(Http404):
            validate_ticker_name("A" * 20)  # Too long

    def test_whitespace_is_trimmed(self):
        """Test whitespace is trimmed from ticker names."""
        assert validate_ticker_name("  PETR4  ") == "PETR4"


class TestValidateBrokerName:
    """Tests for validate_broker_name function."""

    def test_valid_name(self):
        """Test valid broker names are accepted."""
        assert validate_broker_name("XP Investimentos") == "XP Investimentos"
        assert validate_broker_name("Nu Invest") == "Nu Invest"
        assert validate_broker_name("BTG Pactual") == "BTG Pactual"

    def test_none_returns_none(self):
        """Test None input returns None."""
        assert validate_broker_name(None) is None
        assert validate_broker_name("") is None

    def test_invalid_name_raises_404(self):
        """Test invalid broker names raise Http404."""
        with pytest.raises(Http404):
            validate_broker_name("A" * 150)  # Too long

    def test_whitespace_is_normalized(self):
        """Test extra whitespace is normalized."""
        assert validate_broker_name("  XP   Investimentos  ") == "XP Investimentos"


class TestValidateCategoryTitle:
    """Tests for validate_category_title function."""

    def test_valid_category(self):
        """Test valid category titles are accepted."""
        assert validate_category_title("FII") == "FII"
        assert validate_category_title("Ação") == "Ação"
        assert validate_category_title("Stock") == "Stock"
        assert validate_category_title("ETF") == "ETF"

    def test_none_raises_404(self):
        """Test None input raises Http404."""
        with pytest.raises(Http404):
            validate_category_title(None)

        with pytest.raises(Http404):
            validate_category_title("")

    def test_invalid_category_raises_404(self):
        """Test invalid category titles raise Http404."""
        with pytest.raises(Http404):
            validate_category_title("A" * 100)  # Too long


class TestValidatePositiveInteger:
    """Tests for validate_positive_integer function."""

    def test_valid_integer(self):
        """Test valid positive integers are accepted."""
        assert validate_positive_integer(1) == 1
        assert validate_positive_integer("100") == 100
        assert validate_positive_integer(999) == 999

    def test_none_returns_none(self):
        """Test None input returns None."""
        assert validate_positive_integer(None) is None

    def test_zero_raises_404(self):
        """Test zero raises Http404."""
        with pytest.raises(Http404):
            validate_positive_integer(0)

    def test_negative_raises_404(self):
        """Test negative numbers raise Http404."""
        with pytest.raises(Http404):
            validate_positive_integer(-1)

    def test_invalid_value_raises_404(self):
        """Test invalid values raise Http404."""
        with pytest.raises(Http404):
            validate_positive_integer("abc")


class TestValidateYear:
    """Tests for validate_year function."""

    def test_valid_year(self):
        """Test valid years are accepted."""
        assert validate_year(2024) == 2024
        assert validate_year("2023") == 2023
        assert validate_year(2000) == 2000

    def test_none_returns_none(self):
        """Test None input returns None."""
        assert validate_year(None) is None
        assert validate_year("") is None

    def test_invalid_year_raises_404(self):
        """Test invalid years raise Http404."""
        with pytest.raises(Http404):
            validate_year(1800)  # Too old

        with pytest.raises(Http404):
            validate_year(2200)  # Too far in future

        with pytest.raises(Http404):
            validate_year("abc")


class TestValidateMonth:
    """Tests for validate_month function."""

    def test_valid_month(self):
        """Test valid months are accepted."""
        assert validate_month(1) == 1
        assert validate_month("6") == 6
        assert validate_month(12) == 12

    def test_none_returns_none(self):
        """Test None input returns None."""
        assert validate_month(None) is None
        assert validate_month("") is None

    def test_invalid_month_raises_404(self):
        """Test invalid months raise Http404."""
        with pytest.raises(Http404):
            validate_month(0)

        with pytest.raises(Http404):
            validate_month(13)

        with pytest.raises(Http404):
            validate_month("abc")


class TestValidateCurrencyCode:
    """Tests for validate_currency_code function."""

    def test_valid_currency(self):
        """Test valid currency codes are accepted."""
        assert validate_currency_code("BRL") == "BRL"
        assert validate_currency_code("usd") == "USD"
        assert validate_currency_code("EUR") == "EUR"

    def test_none_returns_none(self):
        """Test None input returns None."""
        assert validate_currency_code(None) is None
        assert validate_currency_code("") is None

    def test_invalid_currency_raises_404(self):
        """Test invalid currency codes raise Http404."""
        with pytest.raises(Http404):
            validate_currency_code("USDD")  # Too long

        with pytest.raises(Http404):
            validate_currency_code("US")  # Too short

        with pytest.raises(Http404):
            validate_currency_code("123")  # Numbers

    def test_whitespace_is_trimmed(self):
        """Test whitespace is trimmed from currency codes."""
        assert validate_currency_code("  BRL  ") == "BRL"
