from django.db import models
from django.contrib.auth.models import User
from rosreestr.models import SpatialDataItem


class Purchase(models.Model):
    parcel_index = models.CharField(max_length=100)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)


class PurchaseItem(models.Model):
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item_id = models.ForeignKey(SpatialDataItem, on_delete=models.CASCADE)
    carrier = models.CharField(max_length=20)