from django.db import models

class  Notification (models.Model) : 
    message = models.CharField(max_length= 100 ) 
    
    def  __str__ ( self ): 
        return self.message

from django.contrib.auth.models import User

# gérer et stocker des informations liées aux connexions WebSocket pour chaque utilisateur
class WebSocketConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255, unique=True)
    connected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WebSocket pour {self.user.username} connecté à {self.connected_at}"
