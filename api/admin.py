from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from api.models import Order, OrderItem, User, Product, ProductCategory, ProductSuperCategory, Store, StoreStaff


# Register your models here.

class OrderItemInline(TabularInline):
    model = OrderItem


class OrderAdmin(ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    exclude = ['total_price']


class ProductAdmin(ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'stock', 'store__name', 'in_stock']
    list_filter = ['category', 'stock']
    search_fields = ['name', 'description']
    list_per_page = 20


class ProductCategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'super_category__name', 'description', 'enable']
    search_fields = ['name', 'description']
    list_per_page = 20


class ProductCategoryInline(TabularInline):
    model = ProductCategory


class ProductSuperCategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name', 'description']
    list_per_page = 20
    inlines = [
        ProductCategoryInline
    ]


class StoreUserInline(TabularInline):
    model = StoreStaff


class StoreAdmin(ModelAdmin):
    list_display = ['id', 'name', 'location']
    search_fields = ['name']
    list_per_page = 20
    inlines = [
        StoreUserInline
    ]


class UserAdmin(ModelAdmin):
    model = User


admin.site.register(User, UserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSuperCategory, ProductSuperCategoryAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Order, OrderAdmin)
