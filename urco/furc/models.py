from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


USER_ROLES = {
    ('Admin', 'Admin'),
    ('Research Staff Member', 'Research Staff Member'),
    ('Supervisor', 'Supervisor'),
    ('Higher Approver', 'Higher Approver'),
    ('Order Manager', 'Order Manager'),
    ('Stock Manager', 'Stock Manager')
}

class UserRole(models.Model):
    role_id = models.IntegerField(default=0)
    role_name = models.CharField(choices=USER_ROLES, max_length=100, default="Research Staff Member")

    def __str__(self):
        return self.role_name

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, role=None):
        if not username:
            raise ValueError('The Username field is required')
        if not role:
            raise ValueError('The Role field is required')

        user = self.model(username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, role=None):
        user = self.create_user(username, password, role)
        user.is_admin = True
        user.is_staff = True  # Make superusers staff as well
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add this field
    is_superuser = models.BooleanField(default=False)  # Add this field for admin permissions

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

