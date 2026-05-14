import pytest
from django.urls import reverse
from rest_framework import status

from cats.models import Cat


@pytest.mark.django_db
@pytest.mark.parametrize(
    'fluffiness',
    [0, 11],
)
def test_cat_fluffiness_validator_does_not_pass(
    auth_client,
    cat_data,
    fluffiness,
):
    invalid_data = cat_data.copy()
    invalid_data['fluffiness'] = fluffiness

    response = auth_client.post(
        reverse('cats-list'),
        invalid_data,
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'fluffiness' in response.data
    assert Cat.objects.count() == 0


@pytest.mark.django_db
def test_negative_age_validator_does_not_pass(
    auth_client,
    cat_data,
):
    invalid_data = cat_data.copy()
    invalid_data['age'] = -1

    response = auth_client.post(
        reverse('cats-list'),
        invalid_data,
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'age' in response.data
    assert Cat.objects.count() == 0


@pytest.mark.django_db
def test_cat_name_is_required(
    auth_client,
    cat_data,
):
    invalid_data = cat_data.copy()
    invalid_data.pop('name')

    response = auth_client.post(
        reverse('cats-list'),
        invalid_data,
        format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
    assert Cat.objects.count() == 0
