from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import Memento, MementoCategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class MementoCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MementoCategory
        fields = "__all__"


class MementoSerializer(serializers.ModelSerializer):
    mementoCategory = MementoCategorySerializer()

    class Meta:
        model = Memento
        fields = "__all__"
