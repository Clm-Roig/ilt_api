from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from core.serializers import (
    UserSerializer,
    GroupSerializer,
    MementoSerializer,
    MementoCategorySerializer,
)
from core.models import Memento, MementoCategory
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MementoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mementos to be viewed or edited.
    """

    permission_classes = [IsAuthenticated]
    queryset = Memento.objects.all()
    serializer_class = MementoSerializer


class MementoCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows memento categories to be viewed or edited.
    """

    permission_classes = [IsAuthenticated]
    queryset = MementoCategory.objects.all()
    serializer_class = MementoCategorySerializer
