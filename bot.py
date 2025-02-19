import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand

from db.engine import init_models
from item import crud as item_crud
from keyboards.ikb import builder as ikb
from keyboards.rkb import builder as rkb
from handlers.ikb_handler import router as ikb_router

routers = [
    ikb_router,
]

bot_commands = [
    BotCommand(command='/start', description='Запуск бота'),
    BotCommand(command='/show_items', description='Показать предметы'),
]

dp = Dispatcher()

for r in routers:
    dp.include_router(r)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, {message.from_user.full_name}!",
        reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(Command('show_items'))
async def show_items_by_command(message: Message) -> None:
    items = await item_crud.get_items()
    await message.answer(
        f"Существующие сейчас предметы:\n "
        f"{'\n'.join(map(str, [(item.id, item.data) for item in items]))}"
    )


@dp.message()
async def create_item(message: Message) -> None:
    item_data = message.text
    await item_crud.create_item(data=item_data)
    await message.answer(
        f"Created new item with data: {item_data}.",
        reply_markup=ikb.as_markup())


async def main() -> None:
    bot = Bot(token=getenv('TOKEN'))
    await bot.set_my_commands(bot_commands)
    await init_models()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
