# ❌ DO NOT RUN DIRECTLY
# use: python manage.py run_telegram_bot
import asyncio
import os

import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "hotel_booking_service.settings"
)
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from notifications.models import TelegramSubscriber

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    chat_id = message.chat.id

    TelegramSubscriber.objects.get_or_create(chat_id=chat_id)

    await message.answer(
        "✅ You are subscribed to booking notifications!"
    )

    print("Saved chat_id:", chat_id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
