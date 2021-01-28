from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.models import UserData
from auth_api.utils import isUserAlreadyExistandVerified, isUserInstanceForUpdate, isUserAlreadyExist, validateEmailPhone, generate_random_code, sendVerificationOtp
from django.utils import timezone

class LoginView(APIView):

    authentication_class = ()
    permission_class = ()

    @staticmethod
    def post(request):
        """
        LOGIN User (username is same as email or mobile-number)
        We will maintain custom mapping in userProfile model
        """
        email_phone = request.POST['email_phone']
        if email_phone is None or email_phone == '' or email_phone == '':
            return Response({'error': 'Please provide both email or phone and verification_code'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        if not validateEmailPhone(email_phone):
            return Response({'error': 'Please provide both proper email address or mobile number!'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        userProfile = UserData()
        if isUserAlreadyExistandVerified(email_phone):
            user = isUserInstanceForUpdate(email_phone)
            userProfile = UserData.objects.filter(user=user).first()
            userProfile.verificationOtpCode = generate_random_code(6)
            userProfile.verificationOtpCodeUpdateDate = timezone.now()
            userProfile.save()

            sendVerificationOtp(userProfile.verificationOtpCode, email_phone)

            return Response({"msg": "Otp sent Successfully!", "otp": userProfile.verificationOtpCode},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Login Error!! User does not exist, Please signUp first!!'}, 
                            status=status.HTTP_400_BAD_REQUEST)