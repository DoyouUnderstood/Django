
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Dictionnaire pour suivre les users dans chaque salle et limiter le nombre de participant dans une salle. 
room_participants = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # flag pour savoir si l'utilisateur a été accepté dans la salle, pour eviter les messages de deconnexion alors que refuser dans la salle.
        self.is_participant = False

        if self.room_group_name not in room_participants:
            room_participants[self.room_group_name] = []

        current_participants = room_participants[self.room_group_name] # accept la connexion pour messages d'erreur et deconnecte.
        if len(current_participants) >= 2:
            await self.accept()
            await self.send(text_data=json.dumps({
                'message': 'Erreur : la salle est pleine, vous ne pouvez pas la rejoindre.',
                'username': 'System'
            }))
            
            await self.close()

        else:
            room_participants[self.room_group_name].append(self.scope['user'].username)

            self.is_participant = True

            # Ajouter le canal au groupe WebSocket
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            # Notifier que l'utilisateur a rejoint la salle
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f"{self.scope['user'].username} a rejoint la conversation.",
                    'username': 'System'
                }
            )

    async def disconnect(self, close_code):
        # Si l'utilisateur a été accepté dans la salle, retirer son nom et notifier la deco 
        if self.is_participant:
            if self.room_group_name in room_participants:
                if self.scope['user'].username in room_participants[self.room_group_name]:
                    room_participants[self.room_group_name].remove(self.scope['user'].username)

                    # Si la salle est vide, la supprimer du dictionnaire
                    if len(room_participants[self.room_group_name]) == 0:
                        del room_participants[self.room_group_name]

            # Retirer le canal du groupe WebSocket
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            # Notifier que l'utilisateur a quitté la salle
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f"{self.scope['user'].username} a quitté la conversation.",
                    'username': 'System'
                }
            )

    async def receive(self, text_data):
            # Vérifier si l'utilisateur est toujours dans la salle
            if self.scope['user'].username not in room_participants[self.room_group_name]:
                await self.send(text_data=json.dumps({
                    'error': 'Vous n\'êtes plus dans la salle.'
                }))
                return  # empeche envoi msg 

            # Si l'utilisateur est toujours dans la salle, traiter le msg
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Envoyer le message au client WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))



import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TournamentChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'tournament_chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{self.scope['user'].username} a rejoint le tournoi.",
                'username': 'System'
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{self.scope['user'].username} a quitté le tournoi.",
                'username': 'System'
            }
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps(
        {
            'message': message,
            'username': username
        }))
