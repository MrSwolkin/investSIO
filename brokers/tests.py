"""
Tests for Broker and Currency models and views.
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from brokers.models import Broker, Currency


# ============================================================================
# Fixtures
# ============================================================================

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
def currency_fixture(db):
    """Create a test currency."""
    return Currency.objects.create(code="BRL", name="Real Brasileiro")


@pytest.fixture
def broker_fixture(db, currency_fixture):
    """Create a test broker."""
    return Broker.objects.create(
        name="XP Investimentos",
        currency=currency_fixture,
        country="BR",
        account_number="123456",
        description="Corretora de investimentos"
    )


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


# ============================================================================
# Broker Views Tests
# ============================================================================

class TestBrokerListView:
    """Tests for BrokerListView."""

    def test_list_requires_login(self, client):
        """Test that broker list view requires authentication."""
        response = client.get(reverse('broker_list'))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_list_accessible_when_logged_in(self, authenticated_client):
        """Test that authenticated users can access broker list."""
        response = authenticated_client.get(reverse('broker_list'))
        assert response.status_code == 200

    def test_list_uses_correct_template(self, authenticated_client):
        """Test that broker list uses the correct template."""
        response = authenticated_client.get(reverse('broker_list'))
        assert response.status_code == 200
        assert 'broker_list.html' in [t.name for t in response.templates]

    def test_list_shows_brokers(self, authenticated_client, broker_fixture):
        """Test that broker list shows brokers."""
        response = authenticated_client.get(reverse('broker_list'))
        assert response.status_code == 200
        assert 'brokers' in response.context
        assert broker_fixture in response.context['brokers']

    def test_list_empty_when_no_brokers(self, authenticated_client):
        """Test that broker list shows empty when no brokers exist."""
        response = authenticated_client.get(reverse('broker_list'))
        assert response.status_code == 200
        assert len(response.context['brokers']) == 0

    def test_list_filter_by_name(self, authenticated_client, broker_fixture, db):
        """Test that broker list can be filtered by name."""
        # Create another broker
        Broker.objects.create(name="Banco Inter", country="BR")

        # Filter by XP
        response = authenticated_client.get(reverse('broker_list') + '?name=XP')
        assert response.status_code == 200
        brokers = list(response.context['brokers'])
        assert len(brokers) == 1
        assert brokers[0].name == "XP Investimentos"

    def test_list_filter_by_name_partial_match(self, authenticated_client, broker_fixture):
        """Test that broker list filter works with partial name match."""
        response = authenticated_client.get(reverse('broker_list') + '?name=Invest')
        assert response.status_code == 200
        brokers = list(response.context['brokers'])
        assert len(brokers) == 1

    def test_list_filter_no_results(self, authenticated_client, broker_fixture):
        """Test that broker list filter shows empty results."""
        response = authenticated_client.get(reverse('broker_list') + '?name=NonExistent')
        assert response.status_code == 200
        brokers = list(response.context['brokers'])
        assert len(brokers) == 0


class TestBrokerCreateView:
    """Tests for BrokerCreateView."""

    def test_create_requires_login(self, client):
        """Test that broker create view requires authentication."""
        response = client.get(reverse('broker_create'))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_create_get_form(self, authenticated_client):
        """Test that broker create view shows form on GET."""
        response = authenticated_client.get(reverse('broker_create'))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_create_uses_correct_template(self, authenticated_client):
        """Test that broker create view uses the correct template."""
        response = authenticated_client.get(reverse('broker_create'))
        assert response.status_code == 200
        assert 'broker_create.html' in [t.name for t in response.templates]

    def test_create_post_valid_data(self, authenticated_client, currency_fixture):
        """Test that broker can be created with valid data."""
        data = {
            'name': 'Nu Invest',
            'account_number': '789012',
            'country': 'BR',
            'currency': currency_fixture.pk,
            'description': 'Nova corretora',
        }
        response = authenticated_client.post(reverse('broker_create'), data)
        # Should redirect to broker list on success
        assert response.status_code == 302
        assert reverse('broker_list') in response.url

        # Verify broker was created
        assert Broker.objects.filter(name='Nu Invest').exists()

    def test_create_post_minimal_valid_data(self, authenticated_client):
        """Test that broker can be created with minimal data (just name)."""
        data = {
            'name': 'Minimal Broker',
        }
        response = authenticated_client.post(reverse('broker_create'), data)
        assert response.status_code == 302

        # Verify broker was created
        assert Broker.objects.filter(name='Minimal Broker').exists()

    def test_create_post_invalid_data_empty_name(self, authenticated_client):
        """Test that broker cannot be created without name."""
        data = {
            'name': '',
            'country': 'BR',
        }
        response = authenticated_client.post(reverse('broker_create'), data)
        # Should stay on form page with errors
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors


class TestBrokerDetailsView:
    """Tests for BrokerDetailsView."""

    def test_details_requires_login(self, client, broker_fixture):
        """Test that broker details view requires authentication."""
        response = client.get(reverse('broker_details', kwargs={'pk': broker_fixture.pk}))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_details_get(self, authenticated_client, broker_fixture):
        """Test that broker details view shows broker data."""
        response = authenticated_client.get(
            reverse('broker_details', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200

    def test_details_uses_correct_template(self, authenticated_client, broker_fixture):
        """Test that broker details view uses the correct template."""
        response = authenticated_client.get(
            reverse('broker_details', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200
        assert 'broker_details.html' in [t.name for t in response.templates]

    def test_details_shows_broker_data(self, authenticated_client, broker_fixture):
        """Test that broker details view shows correct broker data."""
        response = authenticated_client.get(
            reverse('broker_details', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200
        assert 'broker' in response.context or 'object' in response.context

    def test_details_404_for_nonexistent_broker(self, authenticated_client):
        """Test that broker details returns 404 for nonexistent broker."""
        response = authenticated_client.get(
            reverse('broker_details', kwargs={'pk': 99999})
        )
        assert response.status_code == 404


class TestBrokerUpdateView:
    """Tests for BrokerUpdateView."""

    def test_update_requires_login(self, client, broker_fixture):
        """Test that broker update view requires authentication."""
        response = client.get(reverse('broker_update', kwargs={'pk': broker_fixture.pk}))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_update_get_form(self, authenticated_client, broker_fixture):
        """Test that broker update view shows form with existing data."""
        response = authenticated_client.get(
            reverse('broker_update', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200
        assert 'form' in response.context

    def test_update_uses_correct_template(self, authenticated_client, broker_fixture):
        """Test that broker update view uses the correct template."""
        response = authenticated_client.get(
            reverse('broker_update', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200
        assert 'broker_update.html' in [t.name for t in response.templates]

    def test_update_form_prepopulated(self, authenticated_client, broker_fixture):
        """Test that broker update form is prepopulated with existing data."""
        response = authenticated_client.get(
            reverse('broker_update', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200
        form = response.context['form']
        assert form.initial['name'] == broker_fixture.name

    def test_update_post_valid_data(self, authenticated_client, broker_fixture):
        """Test that broker can be updated with valid data."""
        data = {
            'name': 'XP Investimentos Atualizada',
            'account_number': broker_fixture.account_number,
            'country': broker_fixture.country,
            'currency': broker_fixture.currency.pk,
            'description': 'Descricao atualizada',
        }
        response = authenticated_client.post(
            reverse('broker_update', kwargs={'pk': broker_fixture.pk}),
            data
        )
        # Should redirect to broker list on success
        assert response.status_code == 302
        assert reverse('broker_list') in response.url

        # Verify broker was updated
        broker_fixture.refresh_from_db()
        assert broker_fixture.name == 'XP Investimentos Atualizada'

    def test_update_post_invalid_data(self, authenticated_client, broker_fixture):
        """Test that broker update fails with invalid data."""
        data = {
            'name': '',  # Name is required
            'country': 'BR',
        }
        response = authenticated_client.post(
            reverse('broker_update', kwargs={'pk': broker_fixture.pk}),
            data
        )
        # Should stay on form page with errors
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_update_404_for_nonexistent_broker(self, authenticated_client):
        """Test that broker update returns 404 for nonexistent broker."""
        response = authenticated_client.get(
            reverse('broker_update', kwargs={'pk': 99999})
        )
        assert response.status_code == 404


class TestBrokerDeleteView:
    """Tests for BrokerDeleteView."""

    def test_delete_requires_login(self, client, broker_fixture):
        """Test that broker delete view requires authentication."""
        response = client.get(reverse('broker_delete', kwargs={'pk': broker_fixture.pk}))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_delete_get_confirmation(self, authenticated_client, broker_fixture):
        """Test that broker delete view shows confirmation page."""
        response = authenticated_client.get(
            reverse('broker_delete', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200

    def test_delete_uses_correct_template(self, authenticated_client, broker_fixture):
        """Test that broker delete view uses the correct template."""
        response = authenticated_client.get(
            reverse('broker_delete', kwargs={'pk': broker_fixture.pk})
        )
        assert response.status_code == 200
        assert 'broker_delete.html' in [t.name for t in response.templates]

    def test_delete_post_deletes_broker(self, authenticated_client, broker_fixture):
        """Test that POST to delete view actually deletes the broker."""
        broker_pk = broker_fixture.pk
        response = authenticated_client.post(
            reverse('broker_delete', kwargs={'pk': broker_pk})
        )
        # Should redirect to broker list on success
        assert response.status_code == 302
        assert reverse('broker_list') in response.url

        # Verify broker was deleted
        assert not Broker.objects.filter(pk=broker_pk).exists()

    def test_delete_404_for_nonexistent_broker(self, authenticated_client):
        """Test that broker delete returns 404 for nonexistent broker."""
        response = authenticated_client.get(
            reverse('broker_delete', kwargs={'pk': 99999})
        )
        assert response.status_code == 404
