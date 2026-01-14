from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from room.models import Room
from room.serializers import RoomSerializer
from room.permissions import IsAdminOrReadOnly


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all().order_by("id")
    serializer_class = RoomSerializer
    permission_classes = (IsAdminOrReadOnly,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("type", "capacity")
