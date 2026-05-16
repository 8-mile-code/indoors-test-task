import json
from json import JSONDecodeError

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
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


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        self.user_group_name = f'user_{self.user.id}'

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name,
            )

    async def send_json(self, payload):
        await self.send(
            text_data=json.dumps(
                payload,
                ensure_ascii=False,
            )
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except JSONDecodeError:
            await self.send_json(
                {
                    'error': 'Invalid JSON format.',
                }
            )
            return

        receiver_id = data.get('receiver_id')
        text = data.get('text')

        if receiver_id is None:
            await self.send_json(
                {
                    'error': 'receiver_id is required.',
                }
            )
            return

        if isinstance(receiver_id, bool):
            await self.send_json(
                {
                    'error': 'receiver_id must be a number.',
                }
            )
            return

        try:
            receiver_id = int(receiver_id)
        except (TypeError, ValueError):
            await self.send_json(
                {
                    'error': 'receiver_id must be a number.',
                }
            )
            return

        if text is None:
            await self.send_json(
                {
                    'error': 'text is required.',
                }
            )
            return

        if not isinstance(text, str):
            await self.send_json(
                {
                    'error': 'text must be a string.',
                }
            )
            return

        text = text.strip()

        if not text:
            await self.send_json(
                {
                    'error': 'text cannot be empty.',
                }
            )
            return

        message = await create_message(
            sender=self.user,
            receiver_id=receiver_id,
            text=text,
        )

        if message is None:
            await self.send_json(
                {
                    'error': 'Receiver not found.',
                }
            )
            return

        payload = {
            'id': message.id,
            'sender_id': self.user.id,
            'sender_username': self.user.username,
            'receiver_id': receiver_id,
            'text': message.text,
            'created_at': message.created_at.isoformat(),
        }

        await self.channel_layer.group_send(
            f'user_{receiver_id}',
            {
                'type': 'chat_message',
                'message': payload,
            }
        )

        await self.send_json(
            {
                'status': 'sent',
                'message': payload,
            }
        )

    async def chat_message(self, event):
        await self.send_json(event['message'])
