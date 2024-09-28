# chat/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def chat_room(request, room_name):
    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'username': request.user.username  
    })

def tournoi_chat_view(request, room_name):
    return render(request, 'tournoi/tournoi.html', {
        'room_name': room_name,
        'username': request.user.username
    })
