from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json, jwt
from django.conf import settings

class RegisterNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = "registerd_users"