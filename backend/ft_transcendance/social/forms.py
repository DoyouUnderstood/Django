from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AddFriendForm(forms.Form):
	user = forms.ModelChoiceField(User.objects.filter(is_active=True))
	friend = forms.ModelChoiceField(User.objects.filter(is_active=True))

	def clean(self):
		cleaned_data = super().clean()
		user = cleaned_data.get('user')
		friend = cleaned_data.get('friend')
		if user.relationships.has_friend(friend):
			self.add_error('friend', 'This friend has already been added')
		return cleaned_data
