from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from userprofile.models import UserProfile, RelationshipActivity
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class GetProfileDataView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, username):
        """
        Fetch profile data of given username, No Auth Required
        """
        print("object passed"+ username)
        
        user = User.objects.filter(username = username).first()
        if not user:
            return Response({'error': 'Oops!! There is No User with that username!!'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        context = {}
        if request.user == user:
            context['is_me'] = True
        else:
            context['is_me'] = False
        
        ### UserProfile 
        userprofile = UserProfile.objects.filter(user = user).first()
        context['profile_data'] = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'date_joined': user.date_joined,
            'email': user.email,
            'mobile': userprofile.mobileNumber,
            'karma': userprofile.karma,
            'description': userprofile.description,
            'followers_count': userprofile.followersCount,
            'following_count': userprofile.followingCount,
            'post_count': userprofile.postCount,
            'profile_picture': userprofile.profilePicture,
            'background_picture': userprofile.backgroundPicture,
            'primary_location': userprofile.primaryLocation,
            'secondary_location': userprofile.secondaryLocation,
            'profile_status': userprofile.profileStatus,
            'account_type': userprofile.profileType
        }

        if not request.user.is_anonymous:
            if len(RelationshipActivity.objects.filter(userFrom = request.user, userTo = user)) > 0:
                context['user_relation_state'] = RelationshipActivity.objects.filter(userFrom = request.user, userTo = user).first().action
            else:
                context['user_relation_state'] = ''
        else:
            context['user_anonymous'] = True

        if request.user.is_authenticated:
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(context, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    
    @staticmethod
    def patch(request, username):
        """
        Update profile of authenticated user
        """
        user = get_object_or_404(User, username=username)
        if request.user != user:
            return Response(context,status=status.HTTP_401_UNAUTHORIZED)
        
        userProfile = get_object_or_404(UserProfile, user=user)


'''
Profile Relation Activity
'''
class ProfileActionView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, username, user_action):
        user = User.objects.filter(username = username).first()
        context = {}
        reln_activity = RelationshipActivity()
        reln_activity.userFrom = request.user
        reln_activity.userTo = user
        if user_action == 'follow':
            reln_activity.action('F')
        elif user_action == 'obsolete':
            reln_activity.action('O')
        elif user_action == 'block':
            reln_activity.action('B')
        elif user_action == 'mute':
            reln_activity.action('M')  
        elif user_action == 'follow_requested':
            reln_activity.action('FR')
        elif user_action == 'follow_mute':
            reln_activity.action('FM')
        elif user_action == 'follow_block':
            reln_activity.action('FB')
        else:
            context['msg'] = user_action + " action is not available!!"

        if 'msg' not in context:
            context['msg'] = user_action + " successfully performed"

        reln_activity.save()
        return Response(context, status=status.HTTP_202_ACCEPTED)

'''
Still Not Sure if this method is needed
'''
class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        print(user.username)
        return Response(user.username)