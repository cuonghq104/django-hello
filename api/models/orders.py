from decimal import Decimal

from django.db import models
import uuid

from .products import Product
from .users import User


class Order(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

    # def save(self, *args, **kwargs):
    #     self.total_price = sum(item.current_price for item in self.products.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def item_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"Product {self.product.name} with quantity {self.quantity}"

    def save(self, *args, **kwargs):
        # Set price to product's current price if not already set
        if not self.price:
            self.price = self.product.current_price
        super().save(*args, **kwargs)