from django.db import models
from django.contrib.auth.models import User

class State(models.TextChoices):
    # States
    ANDHRA_PRADESH = 'AP', 'Andhra Pradesh'
    ARUNACHAL_PRADESH = 'AR', 'Arunachal Pradesh'
    ASSAM = 'AS', 'Assam'
    BIHAR = 'BR', 'Bihar'
    Chhattisgarh = 'CG', 'Chattisgarh'
    GOA = 'GA', 'Goa'
    GUJARAT = 'GJ', 'Gujarat'
    HARYANA = 'HR', 'Haryana'
    HIMACHAL_PRADESH = 'HP', 'Himachal Pradesh'
    JHARKHAND = 'JH', 'Jharkhand'
    KARNATAKA = 'KA', 'Karnataka'
    KERALA = 'KL', 'Kerala'
    MADHYA_PRADESH = 'MP', 'Madhya Pradesh'
    MAHARASHTRA = 'MH', 'Maharashtra'
    MANIPUR = 'MN', 'Manipur'
    MEGHALAYA = 'ML', 'Meghalaya'
    MIZORAM = 'MZ', 'Mizoram'
    NAGALAND = 'NL', 'Nagaland'
    ODISHA = 'OD', 'Odisha'
    PUNJAB = 'PB', 'Punjab'
    RAJASTHAN = 'RJ', 'Rajasthan'
    SIKKIM = 'SK', 'Sikkim'
    TAMIL_NADU = 'TN', 'Tamil Nadu'
    TELANGANA = 'TS', 'Telangana'
    TRIPURA = 'TR', 'Tripura'
    UTTAR_PRADESH = 'UP', 'Uttar Pradesh'
    UTTARAKHAND = 'UK', 'Uttarakhand'
    WEST_BENGAL = 'WB', 'West Bengal'
    # Union Territories
    ANDAMAN_NICOBAR = 'AN', 'Andaman and Nicobar Islands'
    CHANDIGARH = 'CH', 'Chandigarh'
    DADRA_AND_NAGAR_HAVELI_DAMAN_DIU = 'DD', 'Dadra and Nagar Haveli and Daman and Diu'
    DELHI = 'DL', 'Delhi'
    JAMMU_KASHMIR = 'JK', 'Jammu and Kashmir'
    LADAKH = 'LA', 'Ladakh'
    LAKSHADWEEP = 'LD', 'Lakshadweep'
    PUDUCHERRY = 'PY', 'Puducherry'

class Language(models.TextChoices):
    ENGLISH = 'EN', 'English'
    HINDI = 'HI', 'Hindi'

class Media(models.Model):
    image = models.ImageField()

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
    deleted = models.BooleanField(default=False)
    parentPostId = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')
    sharePostId = models.ForeignKey('self', on_delete=models.CASCADE, related_name='shares')
    media = models.ManyToManyField(Media)

class LikesActivity(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    activityTime = models.DateTimeField(auto_now_add=True)
    # TODO(rahul0379): add some more relevant fields here

class PostLocationData(models.Model):
    postId = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='location')
    latitude = models.FloatField()
    longitude = models.FloatField()
    locality = models.CharField(max_length=30)
    state = models.CharField(max_length=2, choices = State.choices)
    district = models.CharField(max_length=30)
