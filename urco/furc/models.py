import uuid
from django.utils import timezone
from random import random

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class UserRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    user_role = models.CharField(max_length=255)

    def __str__(self):
        return self.user_role

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if 'role' not in extra_fields:
            # Set a default role if not provided
            extra_fields['role'] = UserRole.objects.get(user_role='Admin')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if 'role' not in extra_fields:
            # Set a default role for superuser
            extra_fields['role'] = UserRole.objects.get(user_role='Admin')
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, to_field='role_id')
    # password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Institute(models.Model):
    institute_id = models.IntegerField(primary_key=True)
    institute_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.institute_id} - {self.institute_name}'

class ResearchCenter(models.Model):
    center_id = models.CharField(primary_key=True, max_length=10)
    center_name = models.CharField(max_length=255)
    institute_id = models.ForeignKey(Institute, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.center_id} - {self.center_name}'

class Laboratory(models.Model):
    lab_id = models.CharField(primary_key=True, max_length=10)
    lab_name = models.CharField(max_length=50)
    center_id = models.ForeignKey(ResearchCenter, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.lab_id} - {self.lab_name}'

class StorageLocation(models.Model):
    storage_location_id = models.CharField(primary_key=True, max_length=10)
    storage_location_name = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('laboratory', 'researchcenter', 'institute')})
    location_id = models.CharField(max_length=10)
    location_object = GenericForeignKey('content_type', 'location_id')

    def __str__(self):
        return f'{self.storage_location_id} - {self.storage_location_name}'

class StorageLevel(models.Model):
    storage_level_id = models.IntegerField(primary_key=True)
    storage_level = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.storage_level_id} - {self.storage_level}'

class RiskCategory(models.Model):
    risk_category_id = models.IntegerField(primary_key=True)
    risk_category = models.CharField(max_length=20)
    role_id = models.ForeignKey(UserRole, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.risk_category_id} - {self.risk_category}'

class Chemical(models.Model):
    chemical_id = models.CharField(primary_key=True, max_length=10)
    common_name = models.CharField(max_length=50)
    systematic_name = models.CharField(max_length=50)
    risk_category = models.ForeignKey(RiskCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.chemical_id} - {self.common_name}'

ORDER_STATUS = {
    ('Requested', 'Requested'),
    ('Pending approval', 'Pending approval'),
    ('Pending higher approval', 'Pending higher approval'),
    ('Approved by supervisor', 'Approved by supervisor'),
    ('Approved by higher', 'Approved by higher'),
    ('Order in progress', 'Order in progress'),
    ('Ordered', 'Ordered'),
    ('Received', 'Received'),
    ('Stored', 'Stored'),
    ('Delivered', 'Delivered'),
    ('Closed', 'Closed'),
    ('rejected', 'rejected')
}

class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=10)
    exp_name = models.CharField(max_length=100)
    lab_id = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    exp_procedure = models.FileField(upload_to= 'order/exp_procedure')
    risk_assessment = models.FileField(upload_to= 'order/risk_assessment')
    order_date = models.DateField(editable=False, auto_now_add=True)
    updated_date = models.DateField(default=None)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS, default='Requested')
    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.order_id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    chemical_id = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    required_amount = models.IntegerField(default=1)
    uom = models.CharField(max_length=10, null=False, default='ml')

    def __str__(self):
        return f'{self.id} - {self.order_id}'

class Stock(models.Model):
    stock_id = models.CharField(primary_key=True, max_length=10)
    stock_date = models.DateField()

    def __str__(self):
        return self.stock_id

DISPOSAL_STATUS = {
    ('NOT YET', 'Not yet'),
    ('DISPOSED', 'Disposed'),
}

class StockItem(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    chemical_id = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    initial_stock = models.IntegerField(default=0)
    Current_stock = models.IntegerField(default=0)
    uom = models.CharField(max_length=10, null=False, default='ml')
    disposal_date = models.DateField()
    disposal_status = models.CharField(max_length=20, choices=DISPOSAL_STATUS, default='Not yet')
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    storage_level = models.ForeignKey(StorageLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.stock_id}'
