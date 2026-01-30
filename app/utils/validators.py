"""
Input validators for views.

Provides validation functions to prevent injection attacks and ensure data integrity.
"""

import re
from django.http import Http404
from django.shortcuts import get_object_or_404


def validate_ticker_name(ticker_name):
    """
    Validate ticker name parameter.

    Args:
        ticker_name: String to validate as ticker name

    Returns:
        Sanitized ticker name (uppercase, alphanumeric only)

    Raises:
        Http404: If ticker name is invalid
    """
    if not ticker_name:
        return None

    # Remove whitespace and convert to uppercase
    ticker_name = ticker_name.strip().upper()

    # Ticker should be alphanumeric (letters and numbers only)
    # Examples: PETR4, VALE3, BOVA11, AAPL
    if not re.match(r'^[A-Z0-9]{1,10}$', ticker_name):
        raise Http404("Ticker invalido")

    return ticker_name


def validate_broker_name(name):
    """
    Validate broker name parameter.

    Args:
        name: String to validate as broker name

    Returns:
        Sanitized broker name

    Raises:
        Http404: If name is invalid
    """
    if not name:
        return None

    # Remove extra whitespace
    name = ' '.join(name.split())

    # Name should contain only letters, numbers, spaces, and common punctuation
    if not re.match(r'^[\w\s\-\.&áéíóúãõâêîôûàèìòùçÁÉÍÓÚÃÕÂÊÎÔÛÀÈÌÒÙÇ]+$', name, re.UNICODE):
        raise Http404("Nome de corretora invalido")

    # Limit length to prevent abuse
    if len(name) > 100:
        raise Http404("Nome de corretora muito longo")

    return name


def validate_category_title(category_title):
    """
    Validate category title parameter.

    Args:
        category_title: String to validate as category title

    Returns:
        Sanitized category title

    Raises:
        Http404: If category title is invalid
    """
    if not category_title:
        raise Http404("Categoria nao informada")

    # Remove extra whitespace
    category_title = ' '.join(category_title.split())

    # Category should contain only letters, numbers, spaces, and accents
    if not re.match(r'^[\w\s\-áéíóúãõâêîôûàèìòùçÁÉÍÓÚÃÕÂÊÎÔÛÀÈÌÒÙÇ]+$', category_title, re.UNICODE):
        raise Http404("Categoria invalida")

    # Limit length
    if len(category_title) > 50:
        raise Http404("Nome de categoria muito longo")

    return category_title


def validate_positive_integer(value, field_name="valor"):
    """
    Validate that a value is a positive integer.

    Args:
        value: Value to validate
        field_name: Name of field for error message

    Returns:
        Integer value

    Raises:
        Http404: If value is not a positive integer
    """
    if value is None:
        return None

    try:
        int_value = int(value)
        if int_value <= 0:
            raise Http404(f"{field_name} deve ser maior que zero")
        return int_value
    except (ValueError, TypeError):
        raise Http404(f"{field_name} invalido")


def validate_year(year):
    """
    Validate year parameter.

    Args:
        year: String or int to validate as year

    Returns:
        Integer year

    Raises:
        Http404: If year is invalid
    """
    if not year:
        return None

    try:
        year_int = int(year)
        if year_int < 1900 or year_int > 2100:
            raise Http404("Ano invalido")
        return year_int
    except (ValueError, TypeError):
        raise Http404("Ano invalido")


def validate_month(month):
    """
    Validate month parameter.

    Args:
        month: String or int to validate as month

    Returns:
        Integer month (1-12)

    Raises:
        Http404: If month is invalid
    """
    if month is None or month == "":
        return None

    try:
        month_int = int(month)
        if month_int < 1 or month_int > 12:
            raise Http404("Mes invalido")
        return month_int
    except (ValueError, TypeError):
        raise Http404("Mes invalido")


def validate_currency_code(currency):
    """
    Validate currency code parameter.

    Args:
        currency: String to validate as currency code

    Returns:
        Sanitized currency code (uppercase)

    Raises:
        Http404: If currency code is invalid
    """
    if not currency:
        return None

    currency = currency.strip().upper()

    # Currency codes are typically 3 letters (ISO 4217)
    if not re.match(r'^[A-Z]{3}$', currency):
        raise Http404("Codigo de moeda invalido")

    return currency
