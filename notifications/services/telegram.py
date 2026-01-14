import os
from aiogram import Bot
from dotenv import load_dotenv

from notifications.models import TelegramSubscriber

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def send_message_to_all(text: str):
    bot = Bot(token=BOT_TOKEN)

    subscribers = TelegramSubscriber.objects.all()

    for sub in subscribers:
        try:
            await bot.send_message(chat_id=sub.chat_id, text=text)
        except Exception as e:
            print(f"Failed to send to {sub.chat_id}: {e}")