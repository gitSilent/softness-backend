from rest_framework import serializers

from users.models import FavoriteItem
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
    in_favorite = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields="__all__"

    def get_in_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteItem.objects.filter(product=obj, favoritelist__user=user).exists()
        return False

# class ProductShortSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     photos = ProductPhotoSerializer(many=True)
#     class Meta:
#         model = Product
#         fields=["id", "photos", "title"]