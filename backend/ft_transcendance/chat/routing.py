from django.urls import path
from . import consumers

# Routes WebSocket
websocket_urlpatterns = [
    path('ws/chat/<room_name>/', consumers.ChatConsumer.as_asgi()),  # URL WebSocket pour le chat
    path('ws/tournament/<room_name>/', consumers.TournamentChatConsumer.as_asgi()),
]

