from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    company_name = models.CharField(_('company name'), max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ()  # No need to set REQUIRED_FIELDS since you only have the email field

    objects = CustomUserManager()

    def __str__(self):
        return self.email
