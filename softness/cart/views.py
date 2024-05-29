from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer
from products.models import Product


# Create your views here.

class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # print(request.user.pk)
        cart = Cart.objects.get(user__pk=request.user.pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # product_id = self.request.query_params.get("product_id")
        product_id = self.request.data.get("product")
        cart = Cart.objects.get(user=request.user)
        if product_id is None:
            return Response("product_id обязателен", status=status.HTTP_400_BAD_REQUEST)

        try:
            user_items = CartItem.objects.filter(cart__user__pk=request.user.pk)
            item = user_items.get(product__pk=product_id)
            item.amount = item.amount + 1
            item.save()
            serializer = CartItemSerializer(item)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            product = Product.objects.get(pk=product_id)
            serializer = AddCartItemSerializer(data={'product': product.id})
            if serializer.is_valid():
                serializer.save(cart=cart)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data={"detail": "Некорректный ID товара корзины"}, status=status.HTTP_400_BAD_REQUEST)


class CartItemIncreaseAPIView(APIView):
    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def put(self, request, cart_item_id, *args, **kwargs):
        item = self.get_object(pk=cart_item_id)
        item.amount = item.amount + 1
        item.save()
        serializer = CartItemSerializer(item)
        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)


class CartItemDecreaseAPIView(APIView):
    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def put(self, request, cart_item_id, *args, **kwargs):
        item = self.get_object(pk=cart_item_id)
        if (item.amount - 1) <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        item.amount = item.amount - 1
        item.save()
        serializer = CartItemSerializer(item)
        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)



class CartItemAPIView(APIView):
    def get_object(self, pk):
        try:
            print(CartItem.objects.all())
            print(CartItem.objects.get(pk=pk))
            return CartItem.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, cart_item_id, *args, **kwargs):
        item = self.get_object(pk=cart_item_id)
        serializer = CartItemSerializer(item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, cart_item_id, *args, **kwargs):
        item = self.get_object(pk=cart_item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)











        # if product_id:
        #     param_id = product_id
        #     qs = CartItem.objects.filter(cart__user__pk=request.user.pk)
        #     try:
        #         item = qs.get(product__pk=param_id)
        #         item.amount = item.amount + 1
        #         item.save()
        #         serializer = AddCartItemSerializer(item)
        #         return Response(serializer.data)
        #     except CartItem.DoesNotExist:
        #         serializer = AddCartItemSerializer(data=request.data)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return Response(serializer.data, status=status.HTTP_201_CREATED)
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     except Exception as e:
        #         return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        # serializer = AddCartItemSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)