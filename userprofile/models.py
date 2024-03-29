from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

class VerificationLevel(models.TextChoices):
    UNVERIFIED = 'U', 'Unverified'
    VERIFIED = 'V', 'Verified'
    OFFICIAL = 'O', 'Official'

# class SignedUpMethod(models.TextChoices):
#     MOBILE = 'MB', 'Mobile'
#     EMAIL = 'EM', 'Email'
#     OTHER = 'OT', 'Other way not possible'

class ProfileStatus(models.TextChoices):
    INCOMPLETE = 'IN', 'Incomplete'
    PARTIAL = 'PR', 'Partially Complete'
    COMPLETE = 'CO', 'Complete'

class profileType(models.TextChoices):
    NORMAL = 'NM', 'Normal User Account'
    MODERATOR = 'MD', 'Moderator Account'
    GOVT = 'GV', 'Government Institutional Account'
    OFFICIAL = 'OF', 'Official Account'
    CELEBRITY = 'CL', 'Celebrity Account'

class AccountPrivacyType(models.TextChoices):
    PUBLIC = 'PB', 'Public'
    PRIVATE = 'PR', 'Private'
    PROTECTED = 'PO', 'Protected' #Only verified Account can access

class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    TRANS = 'T', 'Transgender'
    SECRET = 'S', 'Prefer not to say'

#(State Management of releations b/w Users)
class RelationshipActivityType(models.TextChoices):
    FOLLOW = 'F', 'Follow' # start follwing 
    OBSOLETE = 'O', 'Obsolete' # some reln existed but now obselete (not deleting for sometime for internal use)
    BLOCK = 'B', 'Block' # Without follow Block
    MUTE = 'M', 'Mute' # Without follow Mute
    FOLLOW_REQUESTED = 'FR', 'Follow Requested', #for private account (not allowed if blocked)
    FOLLOW_MUTE = 'FM', 'Follow Mute', # follows then mutes
    FOLLOW_BLOCK = 'FB', 'Follow Block' #follows then blocks

#ToDO -> change model name to UserProfileData
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    emailVerified = models.BooleanField(default = False)
    mobileVerified = models.BooleanField(default = False)
    userHandle = models.CharField(max_length=30, default='')
    #loginId = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=500, default='')
    mobileNumber = models.CharField(max_length=10, default='') #handle uniquess part in the code
    dateOfBirth = models.DateField(null=True)
    verificationLevel = models.CharField(choices=VerificationLevel.choices, max_length=1, default='U')
    karma = models.IntegerField(default=0)
    followersCount = models.IntegerField(default=0)
    followingCount = models.IntegerField(default=0)
    postCount = models.IntegerField(default=0)
    accountDisabled = models.BooleanField(default=False)
    accountDeleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=Gender.choices, default='S')
    privacy = models.CharField(max_length=2, choices=AccountPrivacyType.choices, default='PB')
    registrationDate = models.DateTimeField(default=timezone.now)
    profileUpdateDate = models.DateTimeField()
    profilePicture = models.CharField(max_length=500, default = 'https://i.pravatar.cc/150?img=6')
    backgroundPicture = models.CharField(max_length=500, default = 'https://picsum.photos/id/1006/3000/2000')
    #signedUpMethod = models.CharField(max_length=2, choices=SignedUpMethod.choices, default='EM')
    verificationOtpCode = models.CharField(max_length = 500, null = True)
    verificationOtpCodeUpdateDate = models.DateTimeField()
    profileStatus = models.CharField(max_length=2, choices=ProfileStatus.choices, default = 'IN')
    profileType = models.CharField(max_length=2, choices=profileType.choices, default='NM')
    primaryLocation = models.CharField(max_length=50, default='BR_Nalanda')
    secondaryLocation = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.user.username
    
class RelationshipActivity(models.Model):
    userFrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'outgoing_relationships')
    userTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'incoming_relationships')
    action = models.CharField(choices=RelationshipActivityType.choices, max_length=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    # TODO(rahul0379): add some more relevant fields here

    class Meta:
        unique_together = ('userFrom', 'userTo')
