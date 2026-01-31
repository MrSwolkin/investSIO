"""
Tests for authentication flow.
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


class TestLoginRequired:
    """Test that views require authentication."""

    def test_home_requires_login(self, client):
        """Test home view redirects unauthenticated users."""
        response = client.get(reverse("home"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_negociations_requires_login(self, client):
        """Test negociations view redirects unauthenticated users."""
        response = client.get(reverse("negociations"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_broker_list_requires_login(self, client):
        """Test broker list view redirects unauthenticated users."""
        response = client.get(reverse("broker_list"))
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_inflow_list_requires_login(self, client):
        """Test inflow list view redirects unauthenticated users."""
        response = client.get(reverse("inflow_list"))
        assert response.status_code == 302
        assert "/login/" in response.url


class TestLoginFlow:
    """Test login functionality."""

    def test_login_page_loads(self, client):
        """Test login page loads successfully."""
        response = client.get(reverse("login"))
        assert response.status_code == 200

    def test_login_with_valid_credentials(self, client, user):
        """Test login with valid credentials."""
        response = client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass123"
        })
        assert response.status_code == 302

    def test_login_with_invalid_credentials(self, client, user):
        """Test login with invalid credentials."""
        response = client.post(reverse("login"), {
            "username": "testuser",
            "password": "wrongpassword"
        })
        assert response.status_code == 200  # Returns to login page with error

    def test_logout(self, authenticated_client):
        """Test logout functionality."""
        response = authenticated_client.post(reverse("logout"))
        assert response.status_code == 302


class TestAuthenticatedAccess:
    """Test access after authentication."""

    def test_home_accessible_after_login(self, authenticated_client, category_fii):
        """Test home view is accessible after login."""
        response = authenticated_client.get(reverse("home"))
        assert response.status_code == 200

    def test_negociations_accessible_after_login(self, authenticated_client):
        """Test negociations view is accessible after login."""
        response = authenticated_client.get(reverse("negociations"))
        assert response.status_code == 200

    def test_broker_list_accessible_after_login(self, authenticated_client):
        """Test broker list view is accessible after login."""
        response = authenticated_client.get(reverse("broker_list"))
        assert response.status_code == 200

    def test_inflow_list_accessible_after_login(self, authenticated_client):
        """Test inflow list view is accessible after login."""
        response = authenticated_client.get(reverse("inflow_list"))
        assert response.status_code == 200
