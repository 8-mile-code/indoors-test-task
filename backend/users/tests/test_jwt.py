import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_can_obtain_jwt_token(api_client, user):
    url = reverse('token_obtain_pair')

    response = api_client.post(
        url,
        {
            'username': 'danil',
            'password': 'testpassword123',
        },
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_user_cannot_get_jwt_token_with_wrong_password(api_client, user):
    url = reverse("token_obtain_pair")

    response = api_client.post(
        url,
        {
            "username": "danil",
            "password": "wrongpassword123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access" not in response.data
    assert "refresh" not in response.data
