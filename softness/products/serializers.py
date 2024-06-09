from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from cart.models import CartItem
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
    in_cart = serializers.SerializerMethodField()
    fav_item_id = serializers.SerializerMethodField()
    # lowered_title = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields="__all__"

    def get_in_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FavoriteItem.objects.filter(product=obj, favoritelist__user=request.user).exists()
        return False

    def get_in_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CartItem.objects.filter(product=obj, cart__user=request.user).exists()
        return False

    def get_fav_item_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                item = FavoriteItem.objects.get(product=obj, favoritelist__user=request.user)
                print(item.id)
                if item:
                    return item.id
            except ObjectDoesNotExist:
                return -1

    # def get_lowered_title(self, obj):
    #     return obj.lowered_title


# class ProductShortSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     photos = ProductPhotoSerializer(many=True)
#     class Meta:
#         model = Product
#         fields=["id", "photos", "title"]