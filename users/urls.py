from django.urls import path
from .views import UpdateUserView, GetProfileDataView, GetUserDataView, GetFollowersListView

urlpatterns = [
    path('update/', UpdateUserView.as_view()),
    path('get_profile/', GetProfileDataView.as_view()),
    path('get_user/', GetUserDataView.as_view()),
    path('get_followers/', GetFollowersListView.as_view()),
]
