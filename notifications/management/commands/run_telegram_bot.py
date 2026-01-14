import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

import django
from django.core.management.base import BaseCommand

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from asgiref.sync import sync_to_async

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "hotel_booking_service.settings"
)
django.setup()

from notifications.models import TelegramSubscriber


class Command(BaseCommand):
    help = "Run telegram bot"

    def handle(self, *args, **options):
        asyncio.run(self.run_bot())

    async def run_bot(self):
        token = os.getenv("TELEGRAM_BOT_TOKEN")

        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

        bot = Bot(token=token)
        dp = Dispatcher()

        @dp.message(CommandStart())
        async def start_handler(message: Message):
            chat_id = message.chat.id

            await sync_to_async(
                TelegramSubscriber.objects.get_or_create
            )(chat_id=chat_id)

            await message.answer(
                "✅ You are subscribed to booking notifications!"
            )

        self.stdout.write(self.style.SUCCESS("🤖 Telegram bot started"))
        await dp.start_polling(bot)