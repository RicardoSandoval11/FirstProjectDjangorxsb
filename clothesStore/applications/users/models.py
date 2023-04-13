from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Managers
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    OCUPATION_CHOICES = [
        ('0', 'Administrator'),
        ('1', 'Worker'),
        ('2', 'Client'),
    ]

    email = models.CharField('Email', max_length=50, unique=True )
    full_name = models.CharField('Full name', max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, blank=False, max_length=1)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    code_register = models.CharField('Register code',max_length=6, blank=True, null=True)
    ocupation = models.CharField(
        max_length=1,
        choices=OCUPATION_CHOICES,
        default='2'
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [ 'full_name' ]

    objects = UserManager()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.full_name