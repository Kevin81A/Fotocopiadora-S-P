from django.urls import path
from .views import (
    CategoryListAPIView, BrandListAPIView, ProductListAPIView,
    ProductDetailAPIView, ServiceRequestListCreateAPIView,
    ContactMessageCreateAPIView, SystemStatsAPIView
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='api-categories'),
    path('brands/', BrandListAPIView.as_view(), name='api-brands'),
    path('products/', ProductListAPIView.as_view(), name='api-products'),
    path('products/<str:id_code>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('services/', ServiceRequestListCreateAPIView.as_view(), name='api-services'),
    path('contact/', ContactMessageCreateAPIView.as_view(), name='api-contact'),
    path('stats/', SystemStatsAPIView.as_view(), name='api-stats'),
]
