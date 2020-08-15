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
import random
import string

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
	def post(self, request):
		try:
			email = request.POST['email']
			password = request.POST['password']
			print("checking user present or not")
			#print(User.objects.filter(username=username).exists())
			#print(isUserExist(username))
			if isUserAlreadyExist(email):
				return HttpResponseBadRequest("User Already Exist", status=409)
			else:
				#ToDO making username and email same (we can genrate unique values also)
				user = User.objects.create_user(username=email, password=password)
				user.email = email
				fullname = request.POST['fullname']
				first_second_name_list = fullname.split(" ")
				user.first_name = first_second_name_list[0]
				if len(first_second_name_list) == 1:
					user.last_name = ''
				else:
					user.last_name = ' '.join(first_second_name_list[1:])
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Invalid request!")
		try:
			user.save()
			signUpUser = User.objects.get(username=email)
			userdata = UserData(user=signUpUser)
			userdata.userHandle = signUpUser.first_name+generate_random_code(4)
			userdata.loginId = signUpUser.username
			#ToDo - Update signedMethod - mobile/email
			userdata.save()
			
			context = {
				'uid' : signUpUser.id,
				'fullname' : ' '.join([signUpUser.first_name, signUpUser.last_name]),
				'email' : signUpUser.email,
				'username' : signUpUser.username
			}
			return JsonResponse(context, safe=False)
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception:
			# log exception
			return HttpResponseServerError("User creation Failed!")


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserView(LoginRequiredMixin, View):
	def post(self, request):
		pass


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
	def post(self, request):
		email = request.POST['email']
		password = request.POST['password']
		username = None
		user = User.objects.filter(email=email).first()
		if user:
			username = user.username
		
		user = authenticate(username=username, password=password)
		print(user)
		if user is not None:
			try:
				if user.is_active:
					login(request, user)
					signInUser = User.objects.get(username=username)
					context = {
						'uid' : signInUser.id,
						'fullname' : ' '.join([signInUser.first_name, signInUser.last_name]),
						'email' : signInUser.email,
						'username' : signInUser.username
					}
					return JsonResponse(context, safe=False)
				else:
					return HttpResponseBadRequest("Account is disabled!!", status=409)
		    	# return auth success response
		    # TODO(Sachin): Better exception handling with approriate particular exceptions
			except Exception as e:
				# return approriate response
				return HttpResponseServerError(e)
		else:
		    # return auth failed response
		    return HttpResponseBadRequest("User not found!!")


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


@method_decorator(csrf_exempt, name='dispatch')
class forgotPassword(View):
	def get(self, request):
		try:
			email = request.GET['email']
			if(isUserAlreadyExist(email)):
				print("user exist, so generate random password")
				new_password = generate_random_code(8)
				user = User.objects.filter(username=email).first()
				user.set_password(new_password)
				user.save()
				return HttpResponse("success")
			else:
				print("user doesn't exist, so let user know that")
				return HttpResponseBadRequest("User not found!")
			
		# TODO(Sachin): Better exception handling with approriate particular exceptions
		except Exception as e:
			# return logout failed response and log the error
			return HttpResponseServerError(e)

# @method_decorator(csrf_exempt, name='dispatch')
# class CheckUserExist(View):
# 	def get(self, request):
# 		try:
# 			email = request.GET['email']
# 			if(isUserAlreadyExist(email)):
# 				return HttpResponse("yes")
# 			else:
# 				return HttpResponse("no")
# 		# TODO(Sachin): Better exception handling with approriate particular exceptions
# 		except Exception as e:
# 			# return logout failed response and log the error
# 			return HttpResponseServerError(e)

def isUserAlreadyExist(username):
	return User.objects.filter(username=username).exists()

def generate_random_code(code_length):
	code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(code_length))
	return code