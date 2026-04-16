from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):
    ROLE_CHOICE= (
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )
    role =models.CharField(max_length = 10, choices= ROLE_CHOICE)
