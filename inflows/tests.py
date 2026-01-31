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


# ============================================================================
# View Tests
# ============================================================================

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


@pytest.fixture
def authenticated_client(user):
    """Create an authenticated test client."""
    client = Client()
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def inflow_fixture(db, ticker, broker):
    """Create a test inflow."""
    return Inflow.objects.create(
        ticker=ticker,
        broker=broker,
        cost_price=Decimal("100.00"),
        quantity=10,
        date=date.today() - timedelta(days=5),
        type="Compra",
    )


class TestInflowListView:
    """Tests for InflowListView."""

    def test_list_requires_login(self, client):
        """Test that inflow list view requires authentication."""
        response = client.get(reverse('inflow_list'))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_list_accessible_when_logged_in(self, authenticated_client):
        """Test that authenticated users can access inflow list."""
        response = authenticated_client.get(reverse('inflow_list'))
        assert response.status_code == 200

    def test_list_uses_correct_template(self, authenticated_client):
        """Test that inflow list uses the correct template."""
        response = authenticated_client.get(reverse('inflow_list'))
        assert response.status_code == 200
        assert 'inflow_list.html' in [t.name for t in response.templates]

    def test_list_shows_inflows(self, authenticated_client, inflow_fixture):
        """Test that inflow list shows inflows."""
        response = authenticated_client.get(reverse('inflow_list'))
        assert response.status_code == 200
        assert 'inflows' in response.context
        assert inflow_fixture in response.context['inflows']

    def test_list_empty_when_no_inflows(self, authenticated_client):
        """Test that inflow list shows empty when no inflows exist."""
        response = authenticated_client.get(reverse('inflow_list'))
        assert response.status_code == 200
        assert len(response.context['inflows']) == 0

    def test_list_filter_by_ticker(self, authenticated_client, inflow_fixture, ticker):
        """Test that inflow list can be filtered by ticker."""
        response = authenticated_client.get(
            reverse('inflow_list') + f'?ticker={ticker.pk}'
        )
        assert response.status_code == 200
        inflows = list(response.context['inflows'])
        assert len(inflows) == 1
        assert inflows[0] == inflow_fixture

    def test_list_filter_by_broker(self, authenticated_client, inflow_fixture, broker):
        """Test that inflow list can be filtered by broker."""
        response = authenticated_client.get(
            reverse('inflow_list') + f'?broker={broker.pk}'
        )
        assert response.status_code == 200
        inflows = list(response.context['inflows'])
        assert len(inflows) == 1

    def test_list_has_pagination(self, authenticated_client):
        """Test that inflow list has pagination context."""
        response = authenticated_client.get(reverse('inflow_list'))
        assert response.status_code == 200
        assert 'page_obj' in response.context


class TestInflowDetailsView:
    """Tests for InflowDetailsView."""

    def test_details_requires_login(self, client, inflow_fixture):
        """Test that inflow details view requires authentication."""
        response = client.get(
            reverse('inflow_details', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_details_get(self, authenticated_client, inflow_fixture):
        """Test that inflow details view shows inflow data."""
        response = authenticated_client.get(
            reverse('inflow_details', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 200

    def test_details_uses_correct_template(self, authenticated_client, inflow_fixture):
        """Test that inflow details view uses the correct template."""
        response = authenticated_client.get(
            reverse('inflow_details', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 200
        assert 'inflow_details.html' in [t.name for t in response.templates]

    def test_details_404_for_nonexistent_inflow(self, authenticated_client):
        """Test that inflow details returns 404 for nonexistent inflow."""
        response = authenticated_client.get(
            reverse('inflow_details', kwargs={'pk': 99999})
        )
        assert response.status_code == 404


class TestInflowCreateView:
    """Tests for InflowCreateView."""

    def test_create_requires_login(self, client):
        """Test that inflow create view requires authentication."""
        response = client.get(reverse('inflow_create'))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_create_get_form(self, authenticated_client):
        """Test that inflow create view shows form on GET."""
        response = authenticated_client.get(reverse('inflow_create'))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_create_uses_correct_template(self, authenticated_client):
        """Test that inflow create view uses the correct template."""
        response = authenticated_client.get(reverse('inflow_create'))
        assert response.status_code == 200
        assert 'inflow_create.html' in [t.name for t in response.templates]

    def test_create_post_valid_data(self, authenticated_client, ticker, broker):
        """Test that inflow can be created with valid data."""
        data = {
            'ticker': ticker.pk,
            'broker': broker.pk,
            'cost_price': '50.00',
            'quantity': '20',
            'date': date.today().strftime('%Y-%m-%d'),
            'type': 'Compra',
            'tax': '0.00',
        }
        response = authenticated_client.post(reverse('inflow_create'), data)
        # Should redirect on success
        assert response.status_code == 302

        # Verify inflow was created
        assert Inflow.objects.filter(ticker=ticker, quantity=20).exists()

    def test_create_post_invalid_data(self, authenticated_client, ticker, broker):
        """Test that inflow cannot be created with invalid data."""
        data = {
            'ticker': ticker.pk,
            'broker': broker.pk,
            'cost_price': '-10.00',  # Invalid negative price
            'quantity': '10',
            'date': date.today().strftime('%Y-%m-%d'),
            'type': 'Compra',
        }
        response = authenticated_client.post(reverse('inflow_create'), data)
        # Should stay on form page with errors
        assert response.status_code == 200
        assert 'form' in response.context


class TestInflowUpdateView:
    """Tests for InflowUpdateView."""

    def test_update_requires_login(self, client, inflow_fixture):
        """Test that inflow update view requires authentication."""
        response = client.get(
            reverse('inflow_update', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_update_get_form(self, authenticated_client, inflow_fixture):
        """Test that inflow update view shows form with existing data."""
        response = authenticated_client.get(
            reverse('inflow_update', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 200
        assert 'form' in response.context

    def test_update_uses_correct_template(self, authenticated_client, inflow_fixture):
        """Test that inflow update view uses the correct template."""
        response = authenticated_client.get(
            reverse('inflow_update', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 200
        assert 'inflow_update.html' in [t.name for t in response.templates]

    def test_update_post_valid_data(self, authenticated_client, inflow_fixture):
        """Test that inflow can be updated with valid data."""
        data = {
            'ticker': inflow_fixture.ticker.pk,
            'broker': inflow_fixture.broker.pk,
            'cost_price': '75.00',
            'quantity': '15',
            'date': inflow_fixture.date.strftime('%Y-%m-%d'),
            'type': 'Compra',
            'tax': '0.00',
        }
        response = authenticated_client.post(
            reverse('inflow_update', kwargs={'pk': inflow_fixture.pk}),
            data
        )
        # Should redirect on success
        assert response.status_code == 302

        # Verify inflow was updated
        inflow_fixture.refresh_from_db()
        assert inflow_fixture.quantity == 15

    def test_update_404_for_nonexistent_inflow(self, authenticated_client):
        """Test that inflow update returns 404 for nonexistent inflow."""
        response = authenticated_client.get(
            reverse('inflow_update', kwargs={'pk': 99999})
        )
        assert response.status_code == 404


class TestInflowDeleteView:
    """Tests for InflowDeleteView."""

    def test_delete_requires_login(self, client, inflow_fixture):
        """Test that inflow delete view requires authentication."""
        response = client.get(
            reverse('inflow_delete', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_delete_get_confirmation(self, authenticated_client, inflow_fixture):
        """Test that inflow delete view shows confirmation page."""
        response = authenticated_client.get(
            reverse('inflow_delete', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 200

    def test_delete_uses_correct_template(self, authenticated_client, inflow_fixture):
        """Test that inflow delete view uses the correct template."""
        response = authenticated_client.get(
            reverse('inflow_delete', kwargs={'pk': inflow_fixture.pk})
        )
        assert response.status_code == 200
        assert 'inflow_delete.html' in [t.name for t in response.templates]

    def test_delete_post_deletes_inflow(self, authenticated_client, inflow_fixture):
        """Test that POST to delete view actually deletes the inflow."""
        inflow_pk = inflow_fixture.pk
        response = authenticated_client.post(
            reverse('inflow_delete', kwargs={'pk': inflow_pk})
        )
        # Should redirect on success
        assert response.status_code == 302

        # Verify inflow was deleted
        assert not Inflow.objects.filter(pk=inflow_pk).exists()

    def test_delete_404_for_nonexistent_inflow(self, authenticated_client):
        """Test that inflow delete returns 404 for nonexistent inflow."""
        response = authenticated_client.get(
            reverse('inflow_delete', kwargs={'pk': 99999})
        )
        assert response.status_code == 404
