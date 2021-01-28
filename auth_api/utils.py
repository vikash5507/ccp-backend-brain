from django.contrib.auth.models import User
from users.models import UserData
import re
import string
import random

def validateEmailPhone(email_phone):
    is_valid = False
    if(isEmail(email_phone)):
        is_valid = True
    elif(isPhoneNumber(email_phone)):
        is_valid = True
    
    if email_phone is None or email_phone == '' or email_phone == ' ':
        is_valid = False
    return is_valid


def isUserAlreadyExistandVerified(email_phone):
        exist_status = False
        if(isEmail(email_phone)):
            user = User.objects.filter(email = email_phone).first()
            if user is not None:
                exist_status = UserData.objects.filter(user = user).first().emailVerified
        else:
            userProfile = UserData.objects.filter(mobileNumber = email_phone).first()
            if userProfile is not None:
                exist_status = userProfile.mobileVerified

        return exist_status

def isUserAlreadyExist(email_phone):
    exist_status = False
    if(isEmail(email_phone)):
        user = User.objects.filter(email = email_phone).first()
        if user is not None:
            exist_status = True
    else:
        userProfile = UserData.objects.filter(mobileNumber = email_phone).first()
        if userProfile is not None:
            exist_status = True
    
    return exist_status

def isUserInstanceForUpdate(email_phone):
    user = User()
    if(isEmail(email_phone)):
        user_temp = User.objects.filter(email = email_phone).first()
        if user is not None:
            user = user_temp
    else:
        userProfile = UserData.objects.filter(mobileNumber = email_phone).first()
        if userProfile is not None:
            user = userProfile.user
    
    return user

def generate_random_code(code_length):
        #code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(code_length))
        code = ''.join(random.choice(string.digits) for _ in range(code_length))
        return code
    
def isEmail(email_phone):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,4}$'
    if re.search(email_regex, email_phone) is None:
        return False
    return True
    
def isPhoneNumber(email_phone):
    #validates India's Phone number
    phone_regex = "^((0091)|(91)|(\+91)|0?)[6-9][0-9]{9}$"
    if re.search(phone_regex, email_phone) is None:
        return False
    return True

def sendVerificationOtp(verificationOtpCode, email_phone):
    #TODO - take into account Locale language selected in App (message should be in that language)
    if isEmail(email_phone):
        sendOtpToEmail(verificationOtpCode, email_phone) #ToDO - implement SMTP push
    else:
        sendOtpToMobile(verificationOtpCode, email_phone) #ToDO - implement Twilio push
        

def sendOtpToEmail(code, email):
    pass

def sendOtpToMobile(cod, phone):
    pass