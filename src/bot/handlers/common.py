from aiogram import types


async def start_handler(message: types.Message):
    await message.answer("Приветствие")

async def help_handler(message: types.Message):
    await message.answer("Здесь будет список доступных команд")