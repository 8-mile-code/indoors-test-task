import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Return DRF API client."""
    return APIClient()


@pytest.fixture
def user(django_user_model):
    """Create regular user."""
    return django_user_model.objects.create_user(
        username='danil',
        password='testpassword123',
    )


@pytest.fixture
def another_user(django_user_model):
    """Create another regular user."""
    return django_user_model.objects.create_user(
        username='ivan',
        password='testpassword123',
    )


@pytest.fixture
def auth_client(user):
    """Return DRF API client with authenticated user."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def cat_data():
    """Return valid cat data."""
    return {
        'name': 'Barsik',
        'age': 2,
        'breed': 'Siberian',
        'fluffiness': 8,
    }
