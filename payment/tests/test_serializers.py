import pytest
from decimal import Decimal
from payment.serializers import PaymentSerializer
from payment.models import Payment
from booking.models import Booking

@pytest.mark.django_db
def test_payment_serializer_serialization():
    booking = Booking.objects.create(guest_name="John Doe")

    payment = Payment.objects.create(
        booking=booking,
        status=Payment.PaymentStatus.PAID,
        type=Payment.PaymentType.BOOKING,
        session_url="https://example.com/session",
        session_id="sess_123",
        money_to_pay=Decimal("150.00")
    )

    serializer = PaymentSerializer(payment)
    data = serializer.data

    assert data["id"] == payment.id
    assert data["booking"] == booking.id
    assert data["status"] == "Paid"
    assert data["type"] == "Booking"
    assert data["session_url"] == "https://example.com/session"
    assert str(data["money_to_pay"]) == "150.00"


@pytest.mark.django_db
def test_payment_serializer_deserialization_valid():
    booking = Booking.objects.create(guest_name="John Doe")

    valid_data = {
        "booking": booking.id
    }

    serializer = PaymentSerializer(data=valid_data)
    assert serializer.is_valid()
    payment = serializer.save(
        type=Payment.PaymentType.BOOKING,
        session_url="https://example.com/session",
        session_id="sess_123",
        money_to_pay=Decimal("100.00")
    )
    assert payment.booking == booking
    assert payment.status == Payment.PaymentStatus.PENDING


@pytest.mark.django_db
def test_payment_serializer_deserialization_invalid():
    invalid_data = {
        "booking": None
    }

    serializer = PaymentSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "booking" in serializer.errors
