from django.contrib import admin

from .models import UserProfile
from .models import RelationshipActivity

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RelationshipActivity)
