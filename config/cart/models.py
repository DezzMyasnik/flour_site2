from django.db import models

from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(models.Model):
    session = models.CharField(max_length=200)
    product_id = models.ManyToManyField(Product,on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ("name",)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.name