from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import UserData, RelationshipActivity, AccountPrivacyType, RelationshipActivityType
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime

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

@method_decorator(csrf_exempt, name='dispatch')
class FollowUserView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username of user to be followed")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			# If user profile is private, then request a follow, else follow directly
			if user.privacy == AccountPrivacyType.PRIVATE:
				relation = RelationshipActivity(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.FOLLOW_REQUESTED)
			else:
				relation = RelationshipActivity(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.FOLLOW)
			relation.save()
		else:
			return HttpResponseNotFound("User to be followed not found!")

@method_decorator(csrf_exempt, name='dispatch')
class UnfollowUserView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username of user to be followed")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.FOLLOW)
			if relation is not None:
				relation.action = RelationshipActivityType.UNFOLLOW
				relation.save()
			else:
				return HttpResponseNotFound("Given relation does not exist!")
		else:
			return HttpResponseNotFound("User to be unfollowed not found!")

@method_decorator(csrf_exempt, name='dispatch')
class AcceptFollowRequestView(LoginRequiredMixin, View):
	def post(self, request):
		user_to = request.user

		try:
			user_from_username = request.GET['user_from_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username of user to be followed")
		user_from = User.objects.get(username=user_from_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.FOLLOW_REQUESTED)
			if relation is not None:
				relation.action = RelationshipActivityType.FOLLOW
				relation.save()
			else:
				return HttpResponseNotFound("Given relation does not exist!")
		else:
			return HttpResponseNotFound("User not found!")

@method_decorator(csrf_exempt, name='dispatch')
class BlockUserView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username of user to be followed")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to)
			if relation is not None:
				relation.action = RelationshipActivityType.BLOCK
			else:
				relation = RelationshipActivity(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.BLOCK)
			relation.save()
		else:
			return HttpResponseNotFound("User to be blocked not found!")

@method_decorator(csrf_exempt, name='dispatch')
class UnblockUserView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username of user to be followed")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivity.BLOCK)
			if relation is not None:
				# kept this as unfollow, this should change to something like OBSELETE which can later be cleaned up from the db via background jobs
				relation.action = RelationshipActivityType.UNFOLLOW
			else:
				return HttpResponseNotFound("No corresponding relation exists!")
			relation.save()
		else:
			return HttpResponseNotFound("User to be blocked not found!")

@method_decorator(csrf_exempt, name='dispatch')
class MuteUserView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username of user to be followed")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to)
			if relation is not None:
				relation.action = RelationshipActivityType.MUTE
			else:
				relation = RelationshipActivity(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.MUTE)
			relation.save()
		else:
			return HttpResponseNotFound("User to be blocked not found!")

@method_decorator(csrf_exempt, name='dispatch')
class UnmuteUserView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username of user to be followed")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivity.MUTE)
			if relation is not None:
				# kept this as unfollow, this should change to something like OBSELETE which can later be cleaned up from the db via background jobs
				relation.action = RelationshipActivityType.UNFOLLOW
			else:
				return HttpResponseNotFound("No corresponding relation exists!")
			relation.save()
		else:
			return HttpResponseNotFound("User to be blocked not found!")