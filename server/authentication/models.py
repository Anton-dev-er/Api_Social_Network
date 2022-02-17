from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_active', True)
        return self.create_user(email, password, **other_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    last_request = models.DateTimeField(verbose_name='Last request:', null=True, blank=True)
    last_login = models.DateTimeField(verbose_name='Last login:', default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def _generate_jwt_token(self):
        token_expires = timedelta(days=settings.TOKEN_EXPIRE_DAYS)
        expire = datetime.utcnow() + token_expires

        token = jwt.encode({
            'id': self.pk,
            'exp': expire,
        }, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return token

    @property
    def token(self):
        return self._generate_jwt_token()
