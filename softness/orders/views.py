from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from users.permissions import IsOwner


# Create your views here.

class OrdersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    @extend_schema(
        request=None,
        responses={200: OrderSerializer, 403: None},
        tags=['orders']
    )
    def get(self, request):

        orders = Order.objects.filter(user__pk=request.user.pk)
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={200: None, 403: None},
        tags=['orders']
    )
    def post(self, request):
        qs = CartItem.objects.filter(cart=request.user.user_cart)
        if qs.count() <= 0:
            return Response(status=403)
        order = Order.objects.create(user=request.user)
        for item in qs:
            print(item)
            product = item.product
            OrderItem.objects.create(
                product=product,
                amount=item.amount,
                order=order).save()
        qs.delete()
        order.save()
        return Response({"order_id":order.id}, status=200)


class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @extend_schema(
        request=None,
        responses={
            204: None,
        },
        tags=['orders'], )
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            self.check_object_permissions(self.request, order)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise Http404

