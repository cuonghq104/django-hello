# Import all models to make them available from api.models
from .products import *
from .categories import *
from .orders import *
from .users import *
from .stores import *

# This allows you to still use:
# from api.models import Product, Order, User
# Instead of:
# from api.models.product import Product
# from api.models.order import Order

__all__ = [
    'Product',
    'ProductCategory',
    'ProductSuperCategory',
    'Order',
    'OrderItem',
    'User',
    'Store',
    'StoreStaff'
]
