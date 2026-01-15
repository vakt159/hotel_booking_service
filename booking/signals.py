from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.models import Booking
from notifications.tasks import send_telegram_notification


@receiver(post_save, sender=Booking)
def booking_created_notification(sender, instance, created, **kwargs):
    if not created:
        return

    message = (
        "🆕 New booking created\n"
        f"User: {instance.user.email}\n"
        f"Room: {instance.room.number}\n"
        f"Check-in: {instance.check_in_date}\n"
        f"Check-out: {instance.check_out_date}\n"
        f"Price per night: {instance.price_per_night}"
    )

    send_telegram_notification.delay(message)