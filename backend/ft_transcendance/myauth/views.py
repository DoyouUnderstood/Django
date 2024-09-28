from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

from .forms import UserSignupForm

def user_to_json(user, avatar=None):
	return {
		"id": user.id,
		"username": user.username,
		"email": user.email,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"avatar": avatar.avatar.url if avatar else None,
	}

class LoginView(View):
	def post(self, request):
		form = AuthenticationForm(request, data=request.POST)
		if (form.is_valid()):
			user = form.get_user()
			login(request, user)
			return JsonResponse({"user": user_to_json(user, user.avatar)})
		else:
			return JsonResponse(form.errors, safe=False, status=422)

class UserSignupView(View):
	def post(self, request):
		form = UserSignupForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return JsonResponse({'user': user_to_json(user, getattr(user, 'avatar', None))}, status=201)
		else:
			return JsonResponse(form.errors, status=422, safe=False)

class LogoutView(View):
	def post(self, request):
		logout(request)
		return JsonResponse({'message': 'The user was logged out'})