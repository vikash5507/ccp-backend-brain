from django.urls import path
#from .views import LoginView, LogoutView, SignupView, UpdateUserView
from auth_api.views.signup import SignupView
from auth_api.views.otpVerify import OtpVerifyView
from auth_api.views.resendOtp import ResendOtpView
from auth_api.views.login import LoginView
from auth_api.views.logout import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', SignupView.as_view()),
    path('otp_verify/', OtpVerifyView.as_view()),
    path('resend_otp/', ResendOtpView.as_view()),
    #path('updateUser/', UpdateUserView.as_view()),
]
