from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import RelationshipActivity, AccountPrivacyType, RelationshipActivityType
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.datastructures import MultiValueDictKeyError


@method_decorator(csrf_exempt, name='dispatch')
class FollowUserView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send username")
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
			return HttpResponseBadRequest("Send username")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.FOLLOW)
			if relation is not None:
				relation.action = RelationshipActivityType.OBSELETE
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
			return HttpResponseBadRequest("Send username")
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
class CancelFollowRequestView(LoginRequiredMixin, View):
	def post(self, request):
		user_from = request.user

		try:
			user_to_username = request.GET['user_to_username']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest("Send usernamee")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivityType.FOLLOW_REQUESTED)
			if relation is not None:
				relation.action = RelationshipActivityType.OBSELETE
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
			return HttpResponseBadRequest("Send usernamee")
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
			return HttpResponseBadRequest("Send usernamee")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivity.BLOCK)
			if relation is not None:
				# kept this as unfollow, this should change to something like OBSELETE which can later be cleaned up from the db via background jobs
				relation.action = RelationshipActivityType.OBSELETE
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
			return HttpResponseBadRequest("Send usernamee")
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
			return HttpResponseBadRequest("Send usernamee")
		user_to = User.objects.get(username=user_to_username)
		if user is not None:
			relation = RelationshipActivity.objects.get(userFrom=user_from, userTo=user_to, action=RelationshipActivity.MUTE)
			if relation is not None:
				# kept this as unfollow, this should change to something like OBSELETE which can later be cleaned up from the db via background jobs
				relation.action = RelationshipActivityType.OBSELETE
			else:
				return HttpResponseNotFound("No corresponding relation exists!")
			relation.save()
		else:
			return HttpResponseNotFound("User to be blocked not found!")