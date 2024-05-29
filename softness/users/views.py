from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, City, FavoriteItem, FavoriteList
from users.permissions import IsOwner
from users.serializers import UserSerializer, CitySerializer, FavoriteListSerializer


# Create your views here.


class CitiesAPIView(APIView):
    pagination_class = None
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

    def get(self, request):
        user = self.get_object(request.user.pk)
        serialiazer = UserSerializer(user)
        return Response(data=serialiazer.data, status=status.HTTP_200_OK)



class FavoriteListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        list = FavoriteList.objects.filter(user=request.user.pk)
        serializer = FavoriteListSerializer(list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FavoriteListItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        try:
            fav_item = FavoriteItem.objects.get(pk=pk)
            self.check_object_permissions(self.request, fav_item.favoritelist)
            fav_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise Http404
