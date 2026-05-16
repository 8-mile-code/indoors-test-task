import pytest
from django.urls import reverse
from rest_framework import status

from chat.models import Message


@pytest.mark.django_db
def test_user_sees_sent_messages(
    auth_client,
    user,
    another_user,
):
    message = Message.objects.create(
        sender=user,
        receiver=another_user,
        text='Привет, Иван!',
    )

    response = auth_client.get(reverse('messages-list'))

    assert response.status_code == status.HTTP_200_OK

    results = response.data['results']

    assert len(results) == 1
    assert results[0]['id'] == message.id
    assert results[0]['sender'] == user.id
    assert results[0]['sender_username'] == user.username
    assert results[0]['receiver'] == another_user.id
    assert results[0]['receiver_username'] == another_user.username
    assert results[0]['text'] == message.text


@pytest.mark.django_db
def test_user_sees_received_messages(
    auth_client,
    user,
    another_user,
):
    message = Message.objects.create(
        sender=another_user,
        receiver=user,
        text='Привет, Данил!',
    )

    response = auth_client.get(reverse('messages-list'))

    assert response.status_code == status.HTTP_200_OK

    results = response.data['results']

    assert len(results) == 1
    assert results[0]['id'] == message.id
    assert results[0]['sender'] == another_user.id
    assert results[0]['sender_username'] == another_user.username
    assert results[0]['receiver'] == user.id
    assert results[0]['receiver_username'] == user.username
    assert results[0]['text'] == message.text


@pytest.mark.django_db
def test_user_does_not_see_unrelated_messages(
    auth_client,
    another_user,
    third_user,
):
    Message.objects.create(
        sender=another_user,
        receiver=third_user,
        text='Чужое сообщение',
    )

    response = auth_client.get(reverse('messages-list'))

    assert response.status_code == status.HTTP_200_OK

    results = response.data['results']

    assert len(results) == 0
