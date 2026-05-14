import json

from channels.generic.websocket import AsyncWebsocketConsumer


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

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.send(
            text_data=json.dumps(
                {
                    'message': data.get('message', ''),
                    'user_id': self.user.id,
                }
            )
        )
