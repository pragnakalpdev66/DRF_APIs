import json, jwt
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from urllib.parse import parse_qs


class AdminNotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = "user_updates"

        # await self.channel_layer.group_add(self.group_name, self.channel_name)
        # await self.accept()

        # self.user = self.scope["user"]
        # self.close()
        
        query_params = parse_qs(self.scope['query_string'].decode())
        token = query_params.get('token', [None])[0]

        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_role = decoded_data.get('role') 
            print("user_role: ",user_role)
            if user_role == 'user':
                await self.close()
            await self.accept()
            await self.channel_layer.group_add("user_updates", self.channel_name)
        except Exception:
            await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notification",
                "message": data 
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["message"]))
