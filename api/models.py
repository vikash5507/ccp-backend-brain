from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db.models import PointField


class VerificationLevel(models.TextChoices):
    UNVERIFIED = 'U', _('Unverified')
    VERIFIED = 'V', _('VERIFIED')
    OFFICIAL = 'O', _('OFFICIAL')

class State(models.TextChoices):
    # States
    ANDHRA_PRADESH = 'AP', _('Andhra Pradesh')
    ARUNACHAL_PRADESH = 'AR', _('Arunachal Pradesh')
    ASSAM = 'AS', _('Assam')
    BIHAR = 'BR', _('Bihar')
    Chhattisgarh = 'CG', _('Chattisgarh')
    GOA = 'GA', _('Goa')
    GUJARAT = 'GJ', _('Gujarat')
    HARYANA = 'HR', _('Haryana')
    HIMACHAL_PRADESH = 'HP', _('Himachal Pradesh')
    JHARKHAND = 'JH', _('Jharkhand')
    KARNATAKA = 'KA', _('Karnataka')
    KERALA = 'KL', _('Kerala')
    MADHYA_PRADESH = 'MP', _('Madhya Pradesh')
    MAHARASHTRA = 'MH', _('Maharashtra')
    MANIPUR = 'MN', _('Manipur')
    MEGHALAYA = 'ML', _('Meghalaya')
    MIZORAM = 'MZ', _('Mizoram')
    NAGALAND = 'NL', _('Nagaland')
    ODISHA = 'OD', _('Odisha')
    PUNJAB = 'PB', _('Punjab')
    RAJASTHAN = 'RJ', _('Rajasthan')
    SIKKIM = 'SK', _('Sikkim')
    TAMIL_NADU = 'TN', _('Tamil Nadu')
    TELANGANA = 'TS', _('Telangana')
    TRIPURA = 'TR', _('Tripura')
    UTTAR_PRADESH = 'UP', _('Uttar Pradesh')
    UTTARAKHAND = 'UK', _('Uttarakhand')
    WEST_BENGAL = 'WB', _('West Bengal')
    # Union Territories
    ANDAMAN_NICOBAR = 'AN', _('Andaman and Nicobar Islands')
    CHANDIGARH = 'CH', _('Chandigarh')
    DADRA_AND_NAGAR_HAVELI_DAMAN_DIU = 'DD', _('Dadra and Nagar Haveli and Daman and Diu')
    DELHI = 'DL', _('Delhi')
    JAMMU_KASHMIR = 'JK', _('Jammu and Kashmir')
    LADAKH = 'LA', _('Ladakh')
    LAKSHADWEEP = 'LD', _('Lakshadweep')
    PUDUCHERRY = 'PY', _('Puducherry')

class Language(models.TextChoices):
    ENGLISH = 'EN', _('English')
    HINDI = 'HI', _('Hindi')

class RelationshipActivityType(models.TextChoices):
    FOLLOW = 'F', _('Follow')
    UNFOLLOW = 'U', _('Unfollow')
    BLOCK = 'B', _('Block')
    MUTE = 'M', _('Mute')
    FOLLOW_REQUESTED = 'FR', _('Follow Requested')

class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    TRANS = 'T', _('Transgender')
    SECRET = 'S', _('Prefer not to say')

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
    mobileNumber = models.PhoneNumberField(blank=True)
    dateOfBirth = models.DateField(null=True)
    verificationLevel = models.CharField(choices=VerificationLevel.choices, max_length=1)
    karma = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    accountDisabled = models.BooleanField(default=False)
    accountDeleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=Gender.choices)


class Relationships(models.Model):
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE)
    following_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    postId = models.CharField(primary_key=True, editable=False, max_length=50)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    creationTime = models.DateTimeField(auto_now_add=True)
    lastModifiedTime = models.DateTimeField(auto_now=True)
    likeCount = models.IntegerField(default=0)
    shareCount = models.IntegerField(default=0)
    replyCount = models.IntegerField(default=0)
    text = models.CharField(max_length=5000)
    language = models.CharField(max_length=5, choices=Language.choices)
    location = PointField()
    locality = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=2, choices = State.choices)
    deleted = models.BooleanField(default=False)
    parentPostId = models.ForeignKey('self', on_delete=models.CASCADE)
    sharePostId = models.ForeignKey('self', on_delete=models.CASCADE)
    media = models.ManyToManyField(Media)

class LikesActivity(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    activityTime = models.DateTimeField(auto_now_add=True)
    # TODO(rahul0379): add some more relevant fields here

class RelationshipActivity(model.Model):
    userIdFrom = models.ForeignKey(User, on_delete=models.CASCADE)
    userIdTo = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.IntegerField(choices=RelationshipActivityType.choices, max_length=2)
    # TODO(rahul0379): add some more relevant fields here

class Media(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()
