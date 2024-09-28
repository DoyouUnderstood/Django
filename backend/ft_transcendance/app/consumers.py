from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import WebSocketConnection
from .db_utils import create_websocket_connection, delete_websocket_connection
from .services import send_friend_request_notification

class AppConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if user.is_authenticated:
            await create_websocket_connection(user.id, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await delete_websocket_connection(self.channel_name)

    async def receive_json(self, content):
        action = content.get("action")
        data = content.get("data", {})

        if action == "friend_request":
            target_username = data.get("username")
            if target_username:
                await send_friend_request_notification(self.scope['user'].username, target_username)
        if action == "match_request":
            target_username = data.get("username")
            if target_username:
                await send_match_request_notification(self.scope['user'].username, target_username)
            

    # async def friend_request_message(self, event):
    #     await self.send_json({
    #         "type": "notification",
    #         "message": event["message"]
    #     })
