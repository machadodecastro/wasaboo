from __future__ import unicode_literals

import re
import warnings

from _mysql import connection
from django import forms
from django.contrib import auth
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)
from django.contrib.auth.models import Permission, Group, PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.signals import user_logged_in
from django.core import validators
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager
from django.forms.widgets import Select
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import six
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=False, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
     
    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u




    
class User(AbstractBaseUser, PermissionsMixin):    
    email = models.EmailField('email', unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    
    is_staff = models.BooleanField('staff', default=False)
    is_active = models.BooleanField('active', default=False)
    is_email_verified = models.BooleanField('E-mail verified', default=False)
    
    date_joined = models.DateTimeField('Date joined', default=timezone.now)
    
    phone = models.CharField('phone', max_length=255, blank=True)
 
    USERNAME_FIELD = 'email'
 
    objects = UserManager()
 
    def get_full_name(self):
        return u' '.join((self.first_name, self.last_name))
    
    def get_short_name(self):
        return self.first_name
  
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = '_usuarios'
