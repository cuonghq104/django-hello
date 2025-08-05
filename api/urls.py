from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.ProductCategoryCreateListApiView.as_view()),
    path('categories/<int:category_id>', views.ProductCategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('categories/<int:category_id>/products', views.ProductByCategoryAPIView.as_view()),
    path('products/', views.ProductListCreateApiView.as_view()),
    path('products/info', views.ProductInfoApiView.as_view()),
    path('products/<int:product_id>', views.ProductDetailApiView.as_view()),
    path('orders/', views.OrderListApiView.as_view()),
    path('user-orders/', views.UserOrderListApiView.as_view(), name='user-orders'),
]
