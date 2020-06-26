from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from users.models import UserData
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

class SignupView(View):
	def post(self, request):
		user = User.objects.create_user(username=request.POST['id'], password=request.POST['password'])
		user.first_name = request.POST['firstName']
		user.last_name = request.POST['lastName']
		try:
			user.save()
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception as e:
			# log exception
			return # return appropriate response

		user_data = UserData(user=user)
		user_data.userHandle = request.POST['handle']
		user_data.loginId = request.POST['loginId']
		user_data.gender = request.POST['gender']
		try:
			user_data.save()
			# return appropriate response
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception as e:
			# return appropriate response
			pass

class UpdateUserView(LoginRequiredMixin, View):
	def post(self, request):
		pass


class LoginView(View):
	def post(self, request):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			try:
				login(request, user)
		    	# return auth success response
		    # TODO(Sachin): Better exception handling with approriate particular exceptions
			except Exception as e:
				# return approriate response
				pass
		else:
		    # return auth failed response
		    pass


class LogoutView(LoginRequiredMixin, View):
	def get(self, request):
		try:
			logout(request)
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception as e:
			# return logout failed response and log the error
			pass