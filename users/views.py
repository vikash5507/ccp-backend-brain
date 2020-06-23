from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from models import UserData

class AuthService():
	def signup_user(self, request, context):
		user = User.objects.create_user(username=request.id, password=request.password)
		user.first_name = request.firstName
		user.last_name = request.lastName
		try:
			user.save()
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception, e:
			# log exception
			return # return appropriate response

		user_data = UserData(user=user)
		# set other fields
	    user_data.userHandle = request.handle 
	    user_data.loginId = request.loginId 
	    user_data.description = request.description 
	    user_data.mobileNumber = request.mobileNumber 
	    user_data.dateOfBirth = request.dateOfBirth 
	    user_data.verificationLevel = request.verificationLevel
	    user_data.gender = request.gender 
	    try:
			user_data.save()
			# return appropriate response
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception, e:
			# return appropriate response

	def login_user(self, request, context):
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
	def logout_user(self, request, context):
		try:
			logout(request)
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception, e:
			# return logout failed response and log the error