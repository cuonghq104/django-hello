from django.contrib import admin
from api.models import Order, OrderItem, User, Product, ProductCategory

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'stock', 'in_stock']
    list_filter = ['category', 'stock']
    search_fields = ['name', 'description']
    list_per_page = 20

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name', 'description']
    list_per_page = 20

admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)