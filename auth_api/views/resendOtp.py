from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.models import UserData
from auth_api.utils import generate_random_code, sendVerificationOtp, validateEmailPhone, isUserAlreadyExist, isEmail
from django.utils import timezone

class ResendOtpView(APIView):

    @staticmethod
    def post(request):
        email_phone = request.POST['email_phone']
        if email_phone is None or email_phone == '' or email_phone == '':
            return Response({'error': 'Please provide both email or phone'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        if not validateEmailPhone(email_phone):
            return Response({'error': 'Please provide both proper email address or mobile number!'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        userProfile = UserData()
        if isUserAlreadyExist(email_phone):
            if isEmail(email_phone):
                user = User.objects.filter(email = email_phone).first()
                if user is not None:
                    userProfile = UserData.objects.filter(user=user).first()
            else:
                userProfile = UserData.objects.filter(mobileNumber = email_phone).first()
        else:
            return Response({'error': 'User does not exist! Please signUp first!!'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        otp_time_lapse = timezone.now() - userProfile.verificationOtpCodeUpdateDate
        if otp_time_lapse.seconds > 120: #TODO value should come from config
            userProfile.verificationOtpCode = generate_random_code(6)
            userProfile.verificationOtpCodeUpdateDate = timezone.now()
            userProfile.save()
        #TODO - what if people click multiple times resend OTP (handle it different to reduce smtp and mobile calls and send same otp) 
        sendVerificationOtp(userProfile.verificationOtpCode, email_phone)
        return Response({"msg": "Otp resent Successfully!", "otp": userProfile.verificationOtpCode}, status=status.HTTP_202_ACCEPTED)

