import pytest
from django.urls import reverse
from rest_framework import status

from cats.models import Cat


@pytest.mark.django_db
def test_anonymous_user_cannot_create_cat(
    api_client,
    cat_data,
):
    response = api_client.post(
        reverse('cats-list'),
        cat_data,
        format='json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Cat.objects.count() == 0


@pytest.mark.django_db
def test_user_can_sees_only_own_cats(
    auth_client,
    user,
    another_user,
    cat_data,
):
    Cat.objects.create(owner=user, **cat_data)

    another_cat_data = cat_data.copy()
    another_cat_data['name'] = 'Murzik'

    Cat.objects.create(owner=another_user, **another_cat_data)

    response = auth_client.get(reverse('cats-list'))

    assert response.status_code == status.HTTP_200_OK

    results = response.data['results']

    assert len(results) == 1
    assert results[0]['name'] == cat_data['name']


@pytest.mark.django_db
def test_user_cannot_get_another_user_cat(
    auth_client,
    another_user,
    cat_data,
):
    cat = Cat.objects.create(owner=another_user, **cat_data)

    response = auth_client.get(
        reverse('cats-detail', kwargs={'pk': cat.pk}),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_cannot_update_another_user_cat(
    auth_client,
    another_user,
    cat_data,
):
    cat = Cat.objects.create(owner=another_user, **cat_data)

    response = auth_client.patch(
        reverse('cats-detail', kwargs={'pk': cat.pk}),
        {
            'name': 'Bulka',
        },
        format='json',
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    cat.refresh_from_db()

    assert cat.name == cat_data['name']


@pytest.mark.django_db
def test_user_cannot_delete_another_user_cat(
    auth_client,
    another_user,
    cat_data,
):
    cat = Cat.objects.create(owner=another_user, **cat_data)

    response = auth_client.delete(
        reverse('cats-detail', kwargs={'pk': cat.pk}),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Cat.objects.filter(pk=cat.pk).exists()
