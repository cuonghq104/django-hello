from django.db import models
from .categories import ProductCategory


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', null=True)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name
