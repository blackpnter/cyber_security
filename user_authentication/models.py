from django.db import models

# Create your models here.

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):

    # create user
    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    # create super user with admin permissions
    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=300, null=True)
    last_name = models.CharField(max_length=300, null=True)
    username = models.CharField(max_length=300, null=True, unique=True, db_index=True)
    email = models.EmailField(max_length=300, unique=True, null=True, db_index=True)
    password = models.CharField(max_length=1000, default='password')
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    login_count = models.IntegerField(null=True, blank=True)
    login_attempt = models.IntegerField(null=True, blank=True, default=0)
    last_login_ip = models.CharField(max_length=300, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'user_authentication_user'