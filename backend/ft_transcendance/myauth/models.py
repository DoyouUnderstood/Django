import os

from django.db import models
from django.contrib.auth import get_user_model

def avatar_upload_path(instance, filename):
	ext = filename.split('.')[-1]
	return f'avatars/{instance.user.username}.{ext}'

class UserAvatar(models.Model):
	User = get_user_model()
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
	avatar = models.ImageField(upload_to=avatar_upload_path)

	def delete(self, *args, **kwargs):
		if self.avatar:
			if os.path.isfile(self.avatar.path):
				os.remove(self.file.path)
		super().delete(*args, **kwargs)