from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from users.models import UserData
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.utils.datastructures import MultiValueDictKeyError

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
	def post(self, request):
		try:
			user = User.objects.create_user(username=request.GET['username'], password=request.GET['password'])
			user.first_name = request.GET['firstName']
			user.last_name = request.GET['lastName']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Invalid request!")
		try:
			user.save()
			userdata = UserData(user=user)
			userdata.userHandle = request.GET['handle']
			userdata.loginId = request.GET['username']
			userdata.save()
			return HttpResponse("Success")
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception as e:
			# log exception
			return HttpResponseServerError("User creation Failed!")


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserView(LoginRequiredMixin, View):
	def post(self, request):
		pass


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
	def post(self, request):
		user = authenticate(username=request.GET['username'], password=request.GET['password'])
		if user is not None:
			try:
				login(request, user)
				return HttpResponse("success")
		    	# return auth success response
		    # TODO(Sachin): Better exception handling with approriate particular exceptions
			except Exception as e:
				# return approriate response
				return HttpResponseServerError(e)
		else:
		    # return auth failed response
		    return HttpResponseBadRequest("User not found!")


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(LoginRequiredMixin, View):
	def get(self, request):
		try:
			logout(request)
			return HttpResponse("success")
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception as e:
			# return logout failed response and log the error
			return HttpResponseServerError(e)