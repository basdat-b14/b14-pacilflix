from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username

class UserPengguna(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pengguna')
    negara_asal = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
