from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import UserAvatar

class UserSignupForm(UserCreationForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	avatar = forms.ImageField(required=False)

	class Meta:
		model = get_user_model()
		fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if get_user_model().objects.filter(email=email).exists():
			raise ValidationError('The email address is already used')
		return email

	def save(self, commit=True):
		user = super().save(commit)
		avatar = self.cleaned_data.get('avatar')
		if (commit and avatar):
			avatar = UserAvatar(user=user, avatar=avatar)
			avatar.save()
		return user

class UserAvatarForm(forms.ModelForm):
	class Meta:
		model = UserAvatar
		fields = ['avatar']