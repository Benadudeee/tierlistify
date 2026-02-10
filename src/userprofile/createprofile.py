from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(blank=True, max_length=200)
    avatar = models.ImageField(upload_to="avatars/%y/%m", default="")

    

@receiver(user_signed_up)
def create_profile_from_user(request, user, **kwargs):
    profile = Profile.objects.get_or_create(user=user)
    profile.save()
    