from django.contrib import admin
from api.models import Order, OrderItem, User, Product, ProductCategory, ProductSuperCategory
from unfold.admin import ModelAdmin

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Show one empty form by default
    fields = ['product', 'quantity', 'price']
    readonly_fields = ['price']  # Make price read-only since it's calculated


class OrderAdmin(ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    exclude = ['total_price']
    readonly_fields = ['order_id', 'created_at']
    
    def save_formset(self, request, form, formset, change):
        """Override to ensure OrderItems are saved properly"""
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

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

class UserAdmin(ModelAdmin):
    model = User

admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSuperCategory, ProductSuperCategoryAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
