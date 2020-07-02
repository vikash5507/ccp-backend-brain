from django.db import models
from django.contrib.auth.models import User
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

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    userHandle = models.CharField(max_length=30, unique=True)
    loginId = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=500, default='')
    mobileNumber = PhoneNumberField(blank=True)
    dateOfBirth = models.DateField(null=True)
    verificationLevel = models.CharField(choices=VerificationLevel.choices, max_length=1, default='U')
    karma = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    accountDisabled = models.BooleanField(default=False)
    accountDeleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=Gender.choices, default='S')

class RelationshipActivity(models.Model):
    userFrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'outgoing_relationships')
    userTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'incoming_relationships')
    action = models.CharField(choices=RelationshipActivityType.choices, max_length=2)
    # TODO(rahul0379): add some more relevant fields here

    class Meta:
        unique_together = ('userFrom', 'userTo')
