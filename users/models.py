from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class VerificationLevel(models.TextChoices):
    UNVERIFIED = 'U', 'Unverified'
    VERIFIED = 'V', 'Verified'
    OFFICIAL = 'O', 'Official'

class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    TRANS = 'T', 'Transgender'
    SECRET = 'S', 'Prefer not to say'

class RelationshipActivityType(models.TextChoices):
    FOLLOW = 'F', 'Follow'
    UNFOLLOW = 'U', 'Unfollow'
    BLOCK = 'B', 'Block'
    MUTE = 'M', 'Mute'
    FOLLOW_REQUESTED = 'FR', 'Follow Requested'

class User(models.Model):
    userId = models.CharField(primary_key=True, editable=False, max_length=50)
    creationTime = models.DateTimeField(auto_now_add=True)
    lastModifiedTime = models.DateTimeField(auto_now=True)
    userHandle = models.CharField(max_length=30, unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    loginId = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    mobileNumber = PhoneNumberField(blank=True)
    dateOfBirth = models.DateField(null=True)
    verificationLevel = models.CharField(choices=VerificationLevel.choices, max_length=1)
    karma = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    accountDisabled = models.BooleanField(default=False)
    accountDeleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=Gender.choices)

class RelationshipActivity(models.Model):
    userIdFrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'outgoing_relationships')
    userIdTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'incoming_relationships')
    action = models.CharField(choices=RelationshipActivityType.choices, max_length=2)
    # TODO(rahul0379): add some more relevant fields here
