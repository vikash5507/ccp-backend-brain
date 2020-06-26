from django.urls import path
from .views import LoginView, LogoutView, SignupView, UpdateUserView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', SignupView.as_view()),
    path('updateUser/', UpdateUserView.as_view()),
]
