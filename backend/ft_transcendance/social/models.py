from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Relationships(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	friends = models.ManyToManyField(
		to='Relationships',
		through='Friendship',
		symmetrical=False,
		related_name='friends_of'
	)

	def has_friend(self, user):
		"""
		Returns a boolean that checks whether another user is a friend or not
		"""
		friend_exists = self.friends.select_related('user').filter(user=user).exists()
		friend_of_exists = self.friends_of.select_related('user').filter(user=user).exists()
		return friend_exists or friend_of_exists

class Friendship(models.Model):
	from_user = models.ForeignKey(Relationships, related_name='friendships_from', on_delete=models.CASCADE)
	to_user = models.ForeignKey(Relationships, related_name='friendships_to', on_delete=models.CASCADE)
	request_date = models.DateField(auto_now_add=True)
	accept_date = models.DateField(null=True, default=None)