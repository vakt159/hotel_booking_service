from notifications.tasks import send_single_telegram_notification
from notifications.models import TelegramSubscriber


def send_message_to_all(text: str) -> None:
    subscribers = TelegramSubscriber.objects.all()

    if not subscribers:
        print("No Telegram subscribers found to send message.")
        return

    for sub in subscribers:
        send_single_telegram_notification.delay(sub.chat_id, text)
    
    print(f"Dispatched {len(subscribers)} single Telegram notification tasks.")
