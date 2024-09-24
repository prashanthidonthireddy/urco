from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import User, UserRole, Institute, ResearchCenter, Laboratory, StorageLocation, StorageLevel, RiskCategory, Chemical, Order, OrderItem, Stock, StockItem


class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ('storage_location_id', 'storage_location_name', 'content_type', 'location_object')

admin.site.register(StorageLocation, StorageLocationAdmin)

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Institute)
admin.site.register(ResearchCenter)
admin.site.register(Laboratory)
admin.site.register(StorageLevel)
admin.site.register(RiskCategory)
admin.site.register(Chemical)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Stock)
admin.site.register(StockItem)