from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer


# Create your views here.

class OrdersAPIView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user__pk=request.user.pk)
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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
        return Response(status=200)
