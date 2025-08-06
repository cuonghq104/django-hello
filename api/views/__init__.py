# Import all views to make them available from api.views
from .product_views import (
    ProductListCreateApiView,
    ProductDetailApiView,
    ProductInfoApiView,
)
from .order_views import (
    OrderViewSet,
)
from .category_views import (
    ProductCategoryCreateListApiView,
    ProductCategoryRetrieveUpdateDestroyAPIView,
    ProductSuperCategoryCreateListApiView,
    ProductSuperCategoryRetrieveUpdateDestroyAPIView
)

# This allows you to still use:
# from api.views import ProductListCreateApiView
# Instead of:
# from api.views.product_views import ProductListCreateApiView

__all__ = [
    'ProductListCreateApiView',
    'ProductDetailApiView',
    'ProductInfoApiView',
    'OrderViewSet',
    'ProductCategoryCreateListApiView',
    'ProductCategoryRetrieveUpdateDestroyAPIView',
    'ProductSuperCategoryCreateListApiView',
    'ProductSuperCategoryRetrieveUpdateDestroyAPIView'
]
