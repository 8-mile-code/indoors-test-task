from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from .models import Message

User = get_user_model()


@database_sync_to_async
def create_message(
    sender: AbstractUser,
    receiver_id: int,
    text: str
) -> Message | None:
    """Create a chat message or return None if receiver does not exist."""
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return None

    return Message.objects.create(
        sender=sender,
        receiver=receiver,
        text=text,
    )
