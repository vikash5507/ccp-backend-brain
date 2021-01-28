from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.models import UserData
from auth_api.utils import isUserAlreadyExistandVerified, generate_random_code, isEmail, isPhoneNumber, sendVerificationOtp, isUserInstanceForUpdate, validateEmailPhone
from django.utils import timezone
#from auth_api.serializers import UserSerializer

class SignupView(APIView):
    authentication_class = ()
    permission_class = ()

    @staticmethod
    def post(request):
        """
        SignUp User (username is same as email or mobile-number)
        We will maintain custom mapping in userProfile model
        """
        email_phone = request.POST['email_phone'] #ToDo can be mobile number also in future 
        #password = request.POST['password']
        fullname = request.POST['fullname']
        if email_phone is None or fullname is None or email_phone == '' or email_phone == '':
            return Response({'error': 'Please provide both email or phone and fullname'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        if not validateEmailPhone(email_phone):
            return Response({'error': 'Please provide both proper email address or mobile number!'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        if isUserAlreadyExistandVerified(email_phone):
            return Response({'error': 'User Already Exist!! Try Logging in'},
                        status=status.HTTP_409_CONFLICT)
        #user = User.objects.create_user(username=email, password=password)
        phone_number = None
        user = isUserInstanceForUpdate(email_phone)
        if user is None:
            print("user doesn't exist") #TODO - implement logging and debug mechanism
            user = User()
        first_second_name_list = fullname.split(" ")
        user.first_name = first_second_name_list[0]
        if len(first_second_name_list) == 1:
            user.last_name = ''
        else:
            user.last_name = ' '.join(first_second_name_list[1:])
        
        c = generate_random_code(8)
        username = first_second_name_list[0] + str(c)
        while len(User.objects.filter(username = username)) > 0:
            c = generate_random_code(8)
            username = first_second_name_list[0] + str(c)
        user.username = username

        if(isEmail(email_phone)):
            user.email = email_phone #TODO - depends on email_phone
        else:
            phone_number = email_phone
        user.set_unusable_password() #ToDO - Marks user having no password
        user.save()

        ### UserProfile Update
        userprofile = UserData.objects.filter(user = user).first()
        if not userprofile:
            userprofile = UserData()
	
        userprofile.user = user
        userprofile.userHandle = user.username
        userprofile.verificationOtpCode = generate_random_code(6)

        if phone_number is not None:
            userprofile.mobileNumber = phone_number
        userprofile.registrationDate = timezone.now()
        userprofile.verificationOtpCodeUpdateDate = timezone.now()
        userprofile.save()
        #ToDO - handle to send this Otp code to Email or Mobile based on SignUpMethod
        sendVerificationOtp(userprofile.verificationOtpCode, email_phone)
        return Response({"msg": "Otp sent Successfully!", "otp": userprofile.verificationOtpCode}, status=status.HTTP_202_ACCEPTED)
        
       


