from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer, FeedbackPostSerializer
from users.permissions import IsOwner


# Create your views here.
class FeedbackAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @extend_schema(
        request=None,
        responses={200: FeedbackSerializer},
        tags=['feedback']
    )
    def get(self, request):
        city = Feedback.objects.filter(user__pk=request.user.pk)
        serializer = FeedbackSerializer(city, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=FeedbackPostSerializer,
        responses={201: None, 400: None},
        tags=['feedback']
    )
    def post(self, request):
        serializer = FeedbackPostSerializer(data={'user':request.user.pk, 'message':request.data.get('message') })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)