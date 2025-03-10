import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user
from .models import User, Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("--- connect websocket ---")
        self.user = await get_user(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Подключение к комнате
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("--- disconnect websocket ---")
        # Отключение от комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']
        # Сохранение сообщения в базе данных
        # room, _ = Room.objects.get_or_create(name=self.room_name)
        # Message.objects.create(room=room, user=user, text=message)
        room = await self.get_room(self.room_name)
        message = await self.save_message(user, room, data['message'])
        # Отправка сообщения в комнату
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

    async def chat_message(self, event):
        # Отправка сообщения обратно на клиент
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @staticmethod
    async def get_room(name):
        return await Room.objects.filter(name=name).afirst()

    @staticmethod
    async def save_message(user, room, message):
        return await Message.objects.acreate(user=user, room=room, text=message)
