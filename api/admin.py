from django.contrib import admin
from api.models import Order, OrderItem, User, Product, ProductCategory, ProductSuperCategory
from unfold.admin import ModelAdmin

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(ModelAdmin):
    inlines = [
        OrderItemInline
    ]

class ProductAdmin(ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'stock', 'in_stock']
    list_filter = ['category', 'stock']
    search_fields = ['name', 'description']
    list_per_page = 20

class ProductCategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'super_category__name', 'description', 'enable']
    search_fields = ['name', 'description']
    list_per_page = 20

class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory

class ProductSuperCategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name', 'description']
    list_per_page = 20
    inlines = [
        ProductCategoryInline
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSuperCategory, ProductSuperCategoryAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
