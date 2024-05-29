from rest_framework import serializers

from products.serializers import ProductSerializer
from users.models import User, City, FavoriteItem, FavoriteList


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    class Meta:
        model = User
        exclude = ["password", "is_superuser", "is_staff", "is_active", "date_joined", "groups", "user_permissions"]




class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = FavoriteItem
        fields = "__all__"

class FavoriteListSerializer(serializers.ModelSerializer):
    items = FavoriteItemSerializer(many=True)
    class Meta:
        model = FavoriteList
        fields = "__all__"