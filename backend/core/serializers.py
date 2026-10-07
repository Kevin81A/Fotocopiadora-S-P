from rest_framework import serializers
from .models import Category, Brand, Product, ServiceRequest, ContactMessage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon_svg']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, default='')

    class Meta:
        model = Product
        fields = [
            'id', 'id_code', 'name', 'category', 'category_slug', 'category_name',
            'brand', 'brand_name', 'price', 'spec', 'stock_status',
            'discount_percent', 'is_featured', 'compatible_models', 'image',
            'created_at'
        ]


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ['id', 'status', 'admin_notes', 'created_at', 'updated_at']

    def validate_client_phone(self, value):
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) < 7:
            raise serializers.ValidationError("Ingresa un número de teléfono válido (mínimo 7 dígitos).")
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ['id', 'is_read', 'created_at']
