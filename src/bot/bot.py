from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from pydantic_settings import BaseSettings

from handlers.common import start_handler, help_handler


class BotConfig(BaseSettings):
    token: str

    class Config:
        env_file = ".env"
        env_prefix = "BOT_"

class BuhBot:

    def __init__(self, config: BotConfig):
        self.config = config
        self.dp = Dispatcher()
        self.bot = Bot(config.token)
        self.register_handlers()

    def register_handlers(self):
        self.dp.message.register(start_handler, CommandStart())
        self.dp.message.register(help_handler)

    async def start(self):
        await self.dp.start_polling(self.bot)