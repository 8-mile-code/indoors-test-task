import pytest
from cats.models import Cat
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_authenticated_user_can_create_cat(
    auth_client,
    user,
    cat_data,
):
    url = reverse('cats-list')

    response = auth_client.post(
        url,
        cat_data,
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == cat_data['name']
    assert response.data['age'] == cat_data['age']
    assert response.data['breed'] == cat_data['breed']
    assert response.data['fluffiness'] == cat_data['fluffiness']

    assert Cat.objects.count() == 1

    cat = Cat.objects.first()
    assert cat.owner == user


@pytest.mark.django_db
def test_authenticated_user_can_get_cat_list(
    auth_client,
    user,
    cat_data,
):
    Cat.objects.create(owner=user, **cat_data)

    response = auth_client.get(reverse('cats-list'))

    assert response.status_code == status.HTTP_200_OK

    results = response.data['results']

    assert len(results) == 1
    assert results[0]['name'] == cat_data['name']


@pytest.mark.django_db
def test_authenticated_user_can_update_own_cat(
    auth_client,
    user,
    cat_data,
):
    cat = Cat.objects.create(owner=user, **cat_data)

    response = auth_client.patch(
        reverse('cats-detail', kwargs={'pk': cat.pk}),
        {
            'name': 'Murzik',
            'age': 4,
        },
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK

    cat.refresh_from_db()

    assert cat.name == 'Murzik'
    assert cat.age == 4


@pytest.mark.django_db
def test_authenticated_user_can_delete_own_cat(
    auth_client,
    user,
    cat_data,
):
    cat = Cat.objects.create(owner=user, **cat_data)

    response = auth_client.delete(
        reverse('cats-detail', kwargs={'pk': cat.pk}),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Cat.objects.filter(pk=cat.pk).exists()
