import json
from django.utils import timezone

from channels.generic.websocket import AsyncWebsocketConsumer
from twisted.protocols.memcache import ClientError

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def chat_message(self,event):
        await self.send(text_data=json.dumps(event))


class ModuleChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['module_id']
        self.room_group_name = f"chat_module_{self.id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_send',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat()
            }
        )

    async def chat_send(self, event):
        await self.send(text_data=json.dumps(event))


class UserConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.slug = self.scope['url_route']['kwargs']['slug']
        self.user = self.scope['user']
        self.users_chat_room = f'chat_{self.slug}'
        await self.channel_layer.group_add(
            self.users_chat_room,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code_code):
        self.channel_layer.group_discard(
            self.users_chat_room,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        await self.channel_layer.group_send(
            self.users_chat_room,
            {
                'type': 'chat_send',
                'user': self.user.username,
                'message': message,
                'datetime': now.isoformat(),
            }
        )

    async def chat_send(self, event):
        await self.send(text_data=json.loads(event))
