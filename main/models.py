from django.db import models
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from b14_pacilflix import settings
# Create your models here.



# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username
