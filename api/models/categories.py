from django.db import models


class ProductSuperCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    enable = models.BooleanField(default=True)
    super_category = models.ForeignKey(ProductSuperCategory, on_delete=models.CASCADE, related_name='categories', null=True)

    def __str__(self):
        return self.name
