from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from users.managers import UserManager
from django.contrib.postgres.fields import JSONField

class Users(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    data = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perms(self, perm_list, obj=None):
        return (self.is_admin and self.is_active)

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name_plural = "Users"
        db_table = 'users'
