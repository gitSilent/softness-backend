from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from products.models import Product
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


class AddFavoriteItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),)
    class Meta:
        model = FavoriteItem
        fields = ("product",)

class FavoriteListSerializer(serializers.ModelSerializer):
    items = FavoriteItemSerializer(many=True)
    class Meta:
        model = FavoriteList
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'city')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if 'first_name' not in attrs or not attrs['first_name']:
            raise serializers.ValidationError({"first_name": "First name is required."})
        if 'last_name' not in attrs or not attrs['last_name']:
            raise serializers.ValidationError({"last_name": "Last name is required."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            city=validated_data.get('city', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user