from django.urls import path
from .views import AuthService

urlpatterns = [
    path('login/', AuthService.login_user()),
    path('logout/', AuthService.logout_user()),
    path('register/', AuthService.signup_user()),
    path('updateUser/', AuthService.update_user_info()),
]
