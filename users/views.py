from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import UserData, RelationshipActivity
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.serializers import serialize

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserView(LoginRequiredMixin, View):
	def post(self, request):
		user = request.user
		userdata = UserData.objects.get(user=user)
		try:
			try:
				userdata.userHandle = request.GET.get('user_handle', userdata.userHandle)
			except IntegrityError as e:
				return HttpResponseBadRequest(e)

			userdata.description = request.GET.get('description', userdata.description)
			userdata.mobileNumber = request.GET.get('mobileNumber', userdata.mobileNumber)
			if 'dateOfBirth' in request.GET:
				userdata.dateOfBirth = datetime.strptime(request.GET.get('dateOfBirth'), '%Y-%m-%d').date()
			userdata.gender = request.GET.get('gender', userdata.gender)
			userdata.save()
			return HttpResponse("success")
		except MultiValueDictKeyError as e:
			return HttpResponseBadRequest(e)


@method_decorator(csrf_exempt, name='dispatch')
class GetProfileDataView(LoginRequiredMixin, View):
	def get(self, request):
		user = request.user
		userdata = UserData.objects.get(user=user)
		return JsonResponse({
			'userHandle':userdata.userHandle,
			'description':userdata.description,
			'mobileNumber':str(userdata.mobileNumber),
			'dateOfBirth':userdata.dateOfBirth,
			'verificationLevel':userdata.verificationLevel,
			'karma':userdata.karma,
			'followers_count':userdata.followers_count,
			'following_count':userdata.following_count,
			'post_count':userdata.post_count,
			'gender':userdata.gender
		})


@method_decorator(csrf_exempt, name='dispatch')
class GetUserDataView(View):
	def get(self, request):
		try:
			username = request.GET['username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username!")
		user = User.objects.get(username=username)
		if user is not None:
			userdata = UserData.objects.get(user=user)

			if userdata.accountDeleted:
				return HttpResponseNotFound("User does not exist!")
			if userdata.accountDisabled:
				return HttpResponseNotFound("User account disabled!")

			return JsonResponse({
				'userHandle':userdata.userHandle,
				'description':userdata.description,
				'mobileNumber':str(userdata.mobileNumber),
				'dateOfBirth':userdata.dateOfBirth,
				'verificationLevel':userdata.verificationLevel,
				'karma':userdata.karma,
				'followers_count':userdata.followers_count,
				'following_count':userdata.following_count,
				'post_count':userdata.post_count,
				'gender':userdata.gender
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
			corresponding_relations = RelationshipActivity.objects.filter(userIdTo=user, action='F')
			if len(corresponding_relations) <= 50:
				next_page_start_index = next_page_start_index + len(corresponding_relations)
			else:
				next_page_start_index = next_page_start_index + 50
				corresponding_relations = corresponding_relations[next_page_start_index : next_page_start_index+50]

			followers_list = [relation.userIdFrom for relation in corresponding_relations]
			serialized_response = '{\"followers\":' + serialize('json', followers_list, cls=DjangoJSONEncoder) + (',\"next_page_start_index\":%x}' % next_page_start_index)
			print (serialized_response)
			return JsonResponse(json.loads(serialized_response), safe=False)
		else:
			return HttpResponseNotFound("User not found!")


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
			corresponding_relations = RelationshipActivity.objects.filter(userIdFrom=user, action='F')
			if len(corresponding_relations) <= 50:
				next_page_start_index = next_page_start_index + len(corresponding_relations)
			else:
				next_page_start_index = next_page_start_index + 50
				corresponding_relations = corresponding_relations[next_page_start_index : next_page_start_index+50]

			followers_list = [relation.userIdTo for relation in corresponding_relations]
			serialized_response = '{\"following\":' + serialize('json', followers_list, cls=DjangoJSONEncoder) + (',\"next_page_start_index\":%x}' % next_page_start_index)
			print (serialized_response)
			return JsonResponse(json.loads(serialized_response), safe=False)
		else:
			return HttpResponseNotFound("User not found!")