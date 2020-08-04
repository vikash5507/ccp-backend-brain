from django.urls import path
from .user_relation_views import FollowUserView, UnfollowUserView, AcceptFollowRequestView, CancelFollowRequestView, BlockUserView, MuteUserView, UnblockUserView, UnmuteUserView
from .views import UpdateUserView, GetProfileDataView, GetUserDataView, GetFollowersListView, GetFollowingListView

urlpatterns = [
    path('update/', UpdateUserView.as_view()),
    path('get_profile/', GetProfileDataView.as_view()),
    path('get_user/', GetUserDataView.as_view()),
    path('follow_user/', FollowUserView.as_view()),
    path('unfollow_user/', UnfollowUserView.as_view()),
    path('accept_follow_request/', AcceptFollowRequestView.as_view()),
    path('cancel_follow_request/', CancelFollowRequestView.as_view()),
    path('block_user/', BlockUserView.as_view()),
    path('unblock_user/', UnblockUserView.as_view()),
    path('mute_user/', MuteUserView.as_view()),
    path('unmute_user/', UnmuteUserView.as_view()),
    path('get_followers/', GetFollowersListView.as_view()),
    path('get_following/', GetFollowingListView.as_view()),
]
