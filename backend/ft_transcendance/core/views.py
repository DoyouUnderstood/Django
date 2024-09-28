from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

class IndexView(View):
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
		return render(request, "core/index.html")