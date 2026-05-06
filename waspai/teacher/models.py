from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    uname = models.CharField(blank=True , max_length = 20)
    def __str__(self):
        return self.user.username
    




