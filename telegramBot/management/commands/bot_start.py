from django.core.management.base import BaseCommand
from aiogram.utils import executor

from telegramBot import bot
from telegramBot.set_bot_commands import set_default_commands



async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        executor.start_polling(bot.dp, on_startup=on_startup)

