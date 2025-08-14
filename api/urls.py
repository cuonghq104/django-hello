from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('categories/', views.ProductSuperCategoryCreateListApiView.as_view()),
    path('categories/<int:category_id>', views.ProductSuperCategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('categories/child', views.ProductCategoryCreateListApiView.as_view()),
    path('categories/child/<int:category_id>', views.ProductCategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('products/', views.ProductListCreateApiView.as_view()),
    path('products/info', views.ProductInfoApiView.as_view()),
    path('products/<int:product_id>', views.ProductDetailApiView.as_view()),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
router.register('users', views.UserViewSet)
router.register('stores', views.StoreViewSet)
urlpatterns += router.urls
