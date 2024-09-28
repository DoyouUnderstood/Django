from channels.db import database_sync_to_async
from .models import WebSocketConnection

@database_sync_to_async
def create_websocket_connection(user_id, channel_name):
    return WebSocketConnection.objects.create(user_id=user_id, channel_name=channel_name)

@database_sync_to_async
def delete_websocket_connection(channel_name):
    return WebSocketConnection.objects.filter(channel_name=channel_name).delete()

@database_sync_to_async
def get_last_connection_by_username(username):
    return WebSocketConnection.objects.filter(user__username=username).last()
