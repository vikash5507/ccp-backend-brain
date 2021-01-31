from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from auth_api.utils import isUserAlreadyExist, validateEmailPhone, generate_random_code, isEmail, isPhoneNumber
from django.utils import timezone

class OtpVerifyView(APIView):
    authentication_class = ()
    permission_class = ()

    @staticmethod
    def post(request):
        """
        Otp Code Verification for both SignUp and Login - passwordless
        """
        email_phone = request.POST['email_phone']
        verification_code = request.POST['otp']
        if email_phone is None or verification_code is None or email_phone == '' or email_phone == '':
            return Response({'error': 'Please provide both email or phone and verification_code'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        if not validateEmailPhone(email_phone):
            return Response({'error': 'Please provide both proper email address or mobile number!'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        userProfile = UserProfile()
        if isUserAlreadyExist(email_phone):
            if isEmail(email_phone):
                user = User.objects.filter(email = email_phone).first()
                if user is not None:
                    userProfile = UserProfile.objects.filter(user=user).first()
            else:
                userProfile = UserProfile.objects.filter(mobileNumber = email_phone).first()
        else:
            return Response({'error': 'User does not exist! Please signUp first!!'}, 
                        status=status.HTTP_400_BAD_REQUEST)

        if userProfile.verificationOtpCode == verification_code:
            otp_time_lapse = timezone.now() - userProfile.verificationOtpCodeUpdateDate
            if otp_time_lapse.seconds > 900: #TODO - otp timeout values should come from config
                return Response({'error': 'Otp code expired!! Try sending it again'},
                            status=status.HTTP_401_UNAUTHORIZED)
            token, _ = Token.objects.get_or_create(user=userProfile.user) #tokenAuth generation
            login(request, userProfile.user) #sessionAuth generation
            if isEmail(email_phone):
                userProfile.emailVerified = True
            else:
                userProfile.mobileVerified = True
            userProfile.save()
            return Response({'token': token.key, 'username': userProfile.user.username}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Otp code did not match!!'},
                            status=status.HTTP_401_UNAUTHORIZED)



