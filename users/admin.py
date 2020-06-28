from django.contrib import admin

from .models import UserData
from .models import RelationshipActivity

# Register your models here.
admin.site.register(UserData)
admin.site.register(RelationshipActivity)
