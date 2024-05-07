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
    date_of_birth = models.DateField(blank=False, null=False)

    