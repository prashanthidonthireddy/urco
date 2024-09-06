from django.contrib import admin
from .models import MyUser, UserRole

admin.site.register(MyUser)
admin.site.register(UserRole)
