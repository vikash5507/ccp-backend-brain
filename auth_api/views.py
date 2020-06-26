from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from users.models import UserData

class AuthService():
	def signup_user(self, request):
		user = User.objects.create_user(username=request.POST['id'], password=request.POST['password'])
		user.first_name = request.POST['firstName']
		user.last_name = request.POST['lastName']
		try:
			user.save()
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception, e:
			# log exception
			return # return appropriate response

		user_data = UserData(user=user)
		# set other fields
	    user_data.userHandle = request.POST['handle'] 
	    user_data.loginId = request.POST['loginId'] 
	    user_data.gender = request.POST['gender'] 
	    try:
			user_data.save()
			# return appropriate response
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception, e:
			# return appropriate response

	def update_user_info(self, request):
		pass


	def login_user(self, request):
		user = authenticate(username=rrequest.username, password=rrequest.password)
		if user is not None:
			try:
				login(request, user)
		    	# return auth success response
		    # TODO(Sachin): Better exception handling with approriate particular exceptions
		    except Exception, e:
		    	# return approriate response
		else:
		    # return auth failed response


	@login_required
	def logout_user(self, request):
		try:
			logout(request)
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception, e:
			# return logout failed response and log the error