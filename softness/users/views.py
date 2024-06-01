from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from users.models import User, City, FavoriteItem, FavoriteList
from users.permissions import IsOwner
from users.serializers import UserSerializer, CitySerializer, FavoriteListSerializer, AddFavoriteItemSerializer


# Create your views here.


class CitiesAPIView(APIView):
    pagination_class = None

    @extend_schema(
        request=None,
        responses={200: CitySerializer(many=True)},
        tags=['users']
    )
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CityAPIView(APIView):
    def get_object(self, pk):
        try:
            return City.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    @extend_schema(
        request=None,
        responses={200: CitySerializer},
        tags=['users']
    )
    def get(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            item = User.objects.get(pk=pk)
            return item
        except ObjectDoesNotExist:
            raise Http404

    @extend_schema(
        request=None,
        responses={200: UserSerializer},
        tags=['users']
    )
    def get(self, request):
        user = self.get_object(request.user.pk)
        serialiazer = UserSerializer(user)
        return Response(data=serialiazer.data, status=status.HTTP_200_OK)



class FavoriteListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_product(self, pk):
        try:
            item = Product.objects.get(pk=pk)
            return item
        except ObjectDoesNotExist:
            raise Http404

    @extend_schema(
        request=None,
        responses={200: FavoriteListSerializer},
        tags=['users']
    )
    def get(self, request):
        list = FavoriteList.objects.filter(user=request.user.pk)
        serializer = FavoriteListSerializer(list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=AddFavoriteItemSerializer,
        responses={200: FavoriteListSerializer},
        tags=['users']
    )
    def post(self, request):
        product_id = self.request.data.get("product_id")
        if product_id is None:
            return Response("product_id обязателен", status=status.HTTP_400_BAD_REQUEST)

        try:
            product_to_post = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            return Response("Product с таким id не найден", status=status.HTTP_404_NOT_FOUND)

        try:
            fav_list = FavoriteList.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response("FavoriteList с таким id не найден", status=status.HTTP_404_NOT_FOUND)

        try:
            fav_item = fav_list.items.get(product__pk=product_id)
            return Response("Данный товар уже находится в избранном", status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            FavoriteItem.objects.create(
                product=product_to_post,
                favoritelist=fav_list
            )
            return Response(status=status.HTTP_201_CREATED)

class FavoriteListItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @extend_schema(
        request=None,
        responses={204: None, 404:None},
        tags=['users']
    )
    def delete(self, request, pk):
        try:
            fav_item = FavoriteItem.objects.get(pk=pk)
            self.check_object_permissions(self.request, fav_item.favoritelist)
            fav_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise Http404
