import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_can_register(api_client):
    url = reverse('register')

    response = api_client.post(
        url,
        {
            'username': "danil",
            'password': 'testpassword123',
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id']
    assert response.data['username'] == 'danil'
    assert 'password' not in response.data


@pytest.mark.django_db
def test_user_cannot_register_with_existing_username(api_client, user):
    url = reverse("register")

    response = api_client.post(
        url,
        {
            "username": "danil",
            "password": "anotherpassword123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_user_cannot_register_with_short_password(api_client):
    url = reverse("register")

    response = api_client.post(
        url,
        {
            "username": "short_password_user",
            "password": "123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data
