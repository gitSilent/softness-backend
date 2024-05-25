from rest_framework import serializers

from .models import Product, Category, ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ["photo"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    photos = ProductPhotoSerializer(many=True)
    class Meta:
        model = Product
        fields="__all__"