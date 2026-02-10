from django.contrib import admin
from .models import TierListPost
from userprofile.createprofile import Profile

admin.site.register(Profile)
admin.site.register(TierListPost)