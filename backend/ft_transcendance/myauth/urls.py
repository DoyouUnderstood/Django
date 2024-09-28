from django.urls import path
from .views import LoginView, UserSignupView, LogoutView

app_name = 'myauth'

urlpatterns = [
	path('login/', LoginView.as_view(), name='login'),
	path('signup/', UserSignupView.as_view(), name='signup'),
	path('logout/', LogoutView.as_view(), name='logout'),
]