from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()


@database_sync_to_async
def create_message(sender, receiver_id, text):
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return None

    return Message.objects.create(
        sender=sender,
        receiver=receiver,
        text=text,
    )
