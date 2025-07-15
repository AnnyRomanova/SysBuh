import asyncio

from dotenv import load_dotenv

from bot import BuhBot, BotConfig


async def main():
    load_dotenv()
    config = BotConfig()
    bot = BuhBot(config)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())