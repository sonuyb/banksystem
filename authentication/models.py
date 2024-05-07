# authentication/models.py
 
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
 
class CustomUser(AbstractUser):
    USER = 'user'
    STAFF = 'staff'
    ADMIN = 'admin'
 
    ROLE_CHOICES = [
        (USER, 'User'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
    ]
 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

class BlacklistedAccessToken(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=True)

    