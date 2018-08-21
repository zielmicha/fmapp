from django.db import models
from django.contrib.auth import models as auth_models

class UserProfile(models.Model):
    user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE, related_name='profile')

    @classmethod
    def get(cls, user):
        return UserProfile.objects.get_or_create(user=user)[0]

class QueuedFile(models.Model):
    uploader = models.ForeignKey(auth_models.User, on_delete=models.SET_NULL, null=True)
    file = models.FileField()
    comment = models.TextField(max_length=2000, blank=True)
    target_dir = models.CharField(max_length=200, default='/')
