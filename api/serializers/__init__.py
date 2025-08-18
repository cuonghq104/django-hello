# Import all serializers to make them available from api.serializers
from .product_serializers import *
from .category_serializers import *
from .order_serializers import *
from .user_serializers import *
from .store_serializers import *

# This allows you to still use:
# from api.serializers import ProductSerializer, OrderSerializer
# Instead of:
# from api.serializers.product_serializers import ProductSerializer

__all__ = [
    'ProductSerializer',
    'ProductSerializerWithCategoryAsObject',
    'ProductCategorySerializer',
    'OrderItemSerializer',
    'OrderSerializer',
    'UserSerializer',
    'UserRegisterSerializer',
    'UserLoginSerializer',
    'StoreSerializer',
    'StoreSimpleSerializer',
    'StoreProductBulkCreateSerializer'
] 