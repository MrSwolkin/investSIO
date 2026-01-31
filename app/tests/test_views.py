"""
Tests for app views (home, negociations).
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def authenticated_client(client, user):
    """Return an authenticated client."""
    client.login(username="testuser", password="testpass123")
    return client


class TestHomeView:
    """Tests for home/dashboard view."""

    def test_home_returns_200(self, authenticated_client, category_fii):
        """Test home view returns 200."""
        response = authenticated_client.get(reverse("home"))
        assert response.status_code == 200

    def test_home_uses_correct_template(self, authenticated_client, category_fii):
        """Test home view uses home.html template."""
        response = authenticated_client.get(reverse("home"))
        assert "home.html" in [t.name for t in response.templates]

    def test_home_context_contains_metrics(self, authenticated_client, category_fii):
        """Test home view context contains expected data."""
        response = authenticated_client.get(reverse("home"))
        assert "total_inflows" in response.context
        assert "total_applied" in response.context


class TestNegociationsView:
    """Tests for negociations view."""

    def test_negociations_returns_200(self, authenticated_client):
        """Test negociations view returns 200."""
        response = authenticated_client.get(reverse("negociations"))
        assert response.status_code == 200

    def test_negociations_uses_correct_template(self, authenticated_client):
        """Test negociations view uses correct template."""
        response = authenticated_client.get(reverse("negociations"))
        assert "negociations.html" in [t.name for t in response.templates]

    def test_negociations_context_contains_transactions(self, authenticated_client):
        """Test negociations view context contains transactions."""
        response = authenticated_client.get(reverse("negociations"))
        assert "transactions" in response.context
        assert "page_obj" in response.context

    def test_negociations_pagination(self, authenticated_client, inflow_fii):
        """Test negociations view has pagination."""
        response = authenticated_client.get(reverse("negociations"))
        assert response.context["page_obj"] is not None


class TestErrorHandlers:
    """Tests for error handlers."""

    def test_404_handler(self, authenticated_client):
        """Test 404 error handler."""
        response = authenticated_client.get("/nonexistent-page/")
        assert response.status_code == 404
