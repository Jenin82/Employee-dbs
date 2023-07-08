# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=36)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, null=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
