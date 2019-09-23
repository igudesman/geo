from django.contrib import admin
from .models import Purchase, PurchaseItem


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_id', 'parcel_index', 'created_at']


class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_id', 'item_id', 'carrier']


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseItem, PurchaseItemAdmin)