from django.db import models


class SpatialDataItem(models.Model):
    """"""
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price_paper = models.DecimalField(decimal_places=2, max_digits=50)
    price_digital = models.DecimalField(decimal_places=2, max_digits=50)

