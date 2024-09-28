from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import Friendship, Relationships
from .forms import AddFriendForm

User = get_user_model()

class AddFriendView(View):
	def post(self, request):
		form = AddFriendForm(user=request.user, friend=request.POST.get('friend'))
		if form.is_valid():
			user = form.cleaned_data.get('user')
			friend = form.cleaned_data.get('friend')
			user_relationships, _ = Relationships.objects.get_or_create(user=user)
			friend_relationships, _ = Relationships.objects.get_or_create(user=friend)
			Friendship.objects.create(from_user=user_relationships, to_user=friend_relationships)
			return JsonResponse({"message": "The friend was added"}, status=201)
		else:
			return JsonResponse(form.errors, safe=False, status=422)