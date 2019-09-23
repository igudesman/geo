from django.contrib import admin
from .models import SpatialDataItem


class SpatialDataItemAdmin(admin.ModelAdmin):
    """"""
    list_display = ['name', 'description', 'price_paper', 'price_digital']


admin.site.register(SpatialDataItem, SpatialDataItemAdmin)

