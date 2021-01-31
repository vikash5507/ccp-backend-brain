from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import UserProfile, RelationshipActivity
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.serializers import serialize
from django.contrib.auth import login, logout

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserView(LoginRequiredMixin, View):
	def post(self, request):
		user = request.user
		userprofile = UserProfile.objects.get(user=user)
		try:
			try:
				userprofile.userHandle = request.GET.get('user_handle', userprofile.userHandle)
			except IntegrityError as e:
				return HttpResponseBadRequest(e)

			userprofile.description = request.GET.get('description', userprofile.description)
			userprofile.mobileNumber = request.GET.get('mobileNumber', userprofile.mobileNumber)
			if 'dateOfBirth' in request.GET:
				userprofile.dateOfBirth = datetime.strptime(request.GET.get('dateOfBirth'), '%Y-%m-%d').date()
			userprofile.gender = request.GET.get('gender', userprofile.gender)
			userprofile.save()
			return HttpResponse("success")
		except MultiValueDictKeyError as e:
			return HttpResponseBadRequest(e)


@method_decorator(csrf_exempt, name='dispatch')
class GetProfileDataView(LoginRequiredMixin, View):
	def get(self, request):
		user = request.user
		print(user)
		if(user.id == None):
			return HttpResponseBadRequest("If not logged in request should not have come!!")
		else:
			userprofile = UserProfile.objects.get(user=user)
			return JsonResponse({
				'userHandle':userprofile.userHandle,
				'description':userprofile.description,
				'mobileNumber':str(userprofile.mobileNumber),
				'dateOfBirth':userprofile.dateOfBirth,
				'verificationLevel':userprofile.verificationLevel,
				'karma':userprofile.karma,
				'followers_count':userprofile.followersCount,
				'following_count':userprofile.followingCount,
				'post_count':userprofile.postCount,
				'gender':userprofile.gender,
				'uid': userprofile.user.id,
				'fullname' : ' '.join([userprofile.user.first_name, userprofile.user.last_name]),
				'email' : userprofile.user.email,
				'username' : userprofile.user.username
			})


@method_decorator(csrf_exempt, name='dispatch')
class GetUserProfileView(View):
	def get(self, request):
		try:
			username = request.GET['username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username!")
		user = User.objects.get(username=username)
		if user is not None:
			userprofile = UserProfile.objects.get(user=user)

			if userprofile.accountDeleted:
				return HttpResponseNotFound("User does not exist!")
			if userprofile.accountDisabled:
				return HttpResponseNotFound("User account disabled!")

			return JsonResponse({
				'userHandle':userprofile.userHandle,
				'description':userprofile.description,
				'mobileNumber':str(userprofile.mobileNumber),
				'dateOfBirth':userprofile.dateOfBirth,
				'verificationLevel':userprofile.verificationLevel,
				'karma':userprofile.karma,
				'followers_count':userprofile.followersCount,
				'following_count':userprofile.followingCount,
				'post_count':userprofile.postCount,
				'gender':userprofile.gender
			})
		else:
			return HttpResponseNotFound("User does not exist!")

# This will paginate the followers with 50 followers per page!
@method_decorator(csrf_exempt, name='dispatch')
class GetFollowersListView(View):
	def get(self, request):
		if request.user and not request.user.is_anonymous:
			user = request.user
		else:
			try:
				username = request.GET['username']
			except MultiValueDictKeyError:
				return HttpResponseBadRequest("Either user should be logged in or send username!")
			user = User.objects.get(username=username)

		if user is not None:
			next_page_start_index = request.GET.get('next_page_start_index', 0)
			next_page_start_index, followers_list = self.get_followers_list(user, next_page_start_index)
			serialized_response = '{\"followers\":' + serialize('json', followers_list, cls=DjangoJSONEncoder) + (',\"next_page_start_index\":%x}' % next_page_start_index)
			return JsonResponse(json.loads(serialized_response), safe=False)
		else:
			return HttpResponseNotFound("User not found!")

	def get_followers_list(self, user, next_page_start_index):
		corresponding_relations = RelationshipActivity.objects.filter(userTo=user, action='F')
		if len(corresponding_relations) <= 50:
			next_page_start_index = next_page_start_index + len(corresponding_relations)
		else:
			next_page_start_index = next_page_start_index + 50
			corresponding_relations = corresponding_relations[next_page_start_index : next_page_start_index+50]

		followers_list = [relation.userFrom for relation in corresponding_relations]
		return (next_page_start_index, followers_list)



@method_decorator(csrf_exempt, name='dispatch')
class GetFollowingListView(View):
	def get(self, request):
		if request.user and not request.user.is_anonymous:
			user = request.user
		else:
			try:
				username = request.GET['username']
			except MultiValueDictKeyError:
				return HttpResponseBadRequest("Either user should be logged in or send username!")
			user = User.objects.get(username=username)

		if user is not None:
			next_page_start_index = request.GET.get('next_page_start_index', 0)
			next_page_start_index, following_list = self.get_following_list(user, next_page_start_index)
			serialized_response = '{\"following\":' + serialize('json', following_list, cls=DjangoJSONEncoder) + (',\"next_page_start_index\":%x}' % next_page_start_index)
			print (serialized_response)
			return JsonResponse(json.loads(serialized_response), safe=False)
		else:
			return HttpResponseNotFound("User not found!")

	def get_following_list(self, user, next_page_start_index):
		print(user)
		corresponding_relations = RelationshipActivity.objects.filter(userFrom=user, action='F')
		print(corresponding_relations)
		if len(corresponding_relations) <= 50:
			next_page_start_index = next_page_start_index + len(corresponding_relations)
		else:
			next_page_start_index = next_page_start_index + 50
			corresponding_relations = corresponding_relations[next_page_start_index : next_page_start_index+50]

		following_list = [relation.userTo for relation in corresponding_relations]
		return (next_page_start_index, following_list)