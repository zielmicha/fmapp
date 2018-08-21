from django.db import models
from django.contrib.admin import models as auth_models

class UserProfile(models.Model):
    user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE, related_name='profile')



    @classmethod
    def get(cls, user):
        return UserProfile.objects.get_or_create(user=user)[0]
