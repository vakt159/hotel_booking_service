import django_filters

from booking.models import Booking


class BookingFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name="check_in_date", lookup_expr="gte"
    )
    to_date = django_filters.DateFilter(
        field_name="check_out_date", lookup_expr="lte"
    )

    room_type = django_filters.CharFilter(
        field_name="room__type", lookup_expr="iexact"
    )

    class Meta:
        model = Booking
        fields = ["user", "room", "status"]
