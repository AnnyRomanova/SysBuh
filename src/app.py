import asyncio
from src.core.log_setiings import setup_logging
import logging
from dotenv import load_dotenv

from src.bot.bot import BuhBot, BotConfig


async def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Запуск бота")
    load_dotenv()
    config = BotConfig()
    bot = BuhBot(config)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())