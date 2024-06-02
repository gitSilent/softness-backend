from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


# Create your views here.


class ProductsAPIView(ListAPIView):
    # permission_classes = [permissions.py.IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = Product.objects.all()
        if self.request.query_params.get("category"):
            category = self.request.query_params.get("category")
            qs = qs.filter(category__slug=category)
        if self.request.query_params.get("min_price"):
            min_price = self.request.query_params.get("min_price")
            qs = qs.filter(price__gte=min_price)
        if self.request.query_params.get("max_price"):
            max_price = self.request.query_params.get("max_price")
            qs = qs.filter(price__lte=max_price)
        return qs

    @extend_schema(
        request=None,
        responses={200: ProductSerializer},
        tags=['products']
    )
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            response.data['total_pages'] = response.data['count'] // self.pagination_class.page_size + (
                1 if response.data['count'] % self.pagination_class.page_size != 0 else 0)
            return response

        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)

class ProductAPIView(APIView):
    def get_object(self, pk):
        try:
            print(Product.objects.get(pk=pk))
            return Product.objects.get(pk=pk)

        except ObjectDoesNotExist:
            raise Http404

    @extend_schema(
        request=None,
        responses={200: ProductSerializer},
        tags=['products']
    )
    def get(self,request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

