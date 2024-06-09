from rest_framework import serializers

from feedback.models import Feedback
from users.models import User
from users.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Feedback
        fields = "__all__"

class FeedbackPostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),)

    class Meta:
        model = Feedback
        fields = "__all__"
