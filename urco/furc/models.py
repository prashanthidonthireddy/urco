from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    user_role = models.CharField(max_length=255)

    def __str__(self):
        return self.user_role

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        if not user_name:
            raise ValueError('The Username field must be set')
        if 'role' not in extra_fields:
            # Set a default role if not provided
            extra_fields['role'] = UserRole.objects.get(user_role='Admin')
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if 'role' not in extra_fields:
            # Set a default role for superuser
            extra_fields['role'] = UserRole.objects.get(user_role='Admin')
        return self.create_user(user_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=255, unique=True, primary_key=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, to_field='role_id')
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_name
