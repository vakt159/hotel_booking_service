from rest_framework import serializers
from booking.models import Booking


class BookingReadSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = (
            "id",
            "room",
            "user",
            "check_in_date",
            "check_out_date",
            "actual_check_out_date",
            "status",
            "price_per_night",
        )


