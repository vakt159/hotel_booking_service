from rest_framework.viewsets import ReadOnlyModelViewSet
from booking.models import Booking
from booking.serializers import BookingReadSerializer


class BookingViewSet(ReadOnlyModelViewSet):
    queryset = Booking.objects.select_related("room", "user")
    serializer_class = BookingReadSerializer

