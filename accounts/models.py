from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class IncUserManager(BaseUserManager):
    def create_user(self, nik, password=None, **extra_fields):
        if not nik:
            raise ValueError("The NIK must be set")
        user = self.model(nik=nik, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nik, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nik, password, **extra_fields)

class IncUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigIntegerField(primary_key=True)
    nik = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = IncUserManager()

    USERNAME_FIELD = 'nik'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'inc_user'
        managed = True  