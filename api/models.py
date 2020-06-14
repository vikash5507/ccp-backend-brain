from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validatiors import RegexValidator
from django.contrib.gis.db.models import PointField

class User(models.Model):
    VERIFICATION_LEVELS = (
        (0, 'UNVERIFIED'),
        (1, 'VERIFIED'),
        (2, 'OFFICIAL'),
    )
    userId = models.CharField(primary_key=True, editable=False)
    creationTime = models.DateTimeField(auto_now_add=True)
    lastModificationTime = models.DateTimeField(auto_now=True)
    userHandle = models.CharField(max_length=30, unique=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    loginId = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    mobileNumber = models.PhoneNumberField(blank=True)
    dateOfBirth = models.DateField()
    verificationLevel = models.IntegerField(choices=VERIFICATION_LEVELS)
    karma = models.IntegerField()
    followers_count = models.IntegerField()
    following_count = models.IntegerField()
    post_count = models.IntegerField()

class Relationships(models.Model):
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE)
    following_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    postId = models.CharField(primary_key=True, editable=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    creationTime = models.DateTimeField(auto_now_add=True)
    lastModifiedTime = models.DateTimeField(auto_now=True)
    likeCount = models.IntegerField()
    shareCount = models.IntegerField()
    replyCount = models.IntegerField()
    text = models.IntegerField(max_length=5000)
    location = PointField()
    locality = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=30)

class LikesActivity(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    activityTime = models.DateTimeField(auto_now_add=True)
    # TODO(rahul0379): add some more relevant fields here

class RelationshipActivity(model.Model):
    RELATIONSHIP_ACTIVITY_TYPES = (
        (0, 'FOLLOW'),
        (1, 'UNFOLLOW'),
        (2, 'BLOCK'),
        (3, 'MUTE'),
    )
    userIdFrom = models.ForeignKey(User, on_delete=models.CASCADE)
    userIdTo = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.IntegerField(choices=RELATIONSHIP_ACTIVITY_TYPES)
    # TODO(rahul0379): add some more relevant fields here
