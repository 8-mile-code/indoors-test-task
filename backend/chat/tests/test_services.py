import pytest
from asgiref.sync import async_to_sync

from chat.consumers import create_message
from chat.models import Message


@pytest.mark.django_db
def test_create_message_creates_message(user, another_user):
    message = async_to_sync(create_message)(
        sender=user,
        receiver_id=another_user.id,
        text='Привет!',
    )

    assert message is not None
    assert message.sender == user
    assert message.receiver == another_user
    assert message.text == 'Привет!'
    assert Message.objects.count() == 1


@pytest.mark.django_db
def test_create_message_returns_none_for_unknown_receiver(user):
    message = async_to_sync(create_message)(
        sender=user,
        receiver_id=999,
        text='Привет!',
    )

    assert message is None
    assert Message.objects.count() == 0
