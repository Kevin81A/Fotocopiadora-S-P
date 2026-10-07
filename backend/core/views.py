from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Category, Brand, Product, ServiceRequest, ContactMessage
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer,
    ServiceRequestSerializer, ContactMessageSerializer
)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'brand').all()
        cat = self.request.query_params.get('cat', None)
        brand = self.request.query_params.get('brand', None)
        model = self.request.query_params.get('model', None)
        search = self.request.query_params.get('search', None)
        featured = self.request.query_params.get('featured', None)

        if cat and cat != 'all':
            queryset = queryset.filter(category__slug=cat)
        if brand:
            queryset = queryset.filter(brand__name__iexact=brand)
        if model:
            queryset = queryset.filter(compatible_models__icontains=model)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(spec__icontains=search) |
                Q(compatible_models__icontains=search) |
                Q(id_code__icontains=search)
            )
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id_code'


class ServiceRequestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email', None)
        if email:
            return ServiceRequest.objects.filter(client_email__iexact=email)
        return ServiceRequest.objects.all()


class ContactMessageCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


class SystemStatsAPIView(APIView):
    def get(self, request):
        data = {
            'total_products': Product.objects.count(),
            'total_categories': Category.objects.count(),
            'pending_services': ServiceRequest.objects.filter(status='Pendiente').count(),
            'completed_services': ServiceRequest.objects.filter(status='Completada').count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        }
        return Response(data, status=status.HTTP_200_OK)
