import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from db.engine import create_models
from item import crud as item_crud
from keyboards.ikb import builder as ikb
from keyboards.rkb import builder as rkb


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello!",
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


async def on_startup(bot: Bot):
    await create_models()
    # await bot.send_message(ADMIN_ID, 'Bot has been started.')
    print('Started')


async def on_shutdown(bot: Bot):
    # await delete_models()
    # await bot.send_message(ADMIN_ID, 'Bot has been shut down.')
    print('Stopped')


async def main() -> None:
    from routing import r_
    from commands import base_commands

    dp.include_router(r_)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    bot = Bot(token=getenv('TOKEN'))

    await bot.set_my_commands(base_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
