from aiogram import Router, F
from aiogram.types import CallbackQuery

from item import crud as items_crud


router = Router()


@router.callback_query(F.data == 'show_items_callback')
async def show_items(callback_query: CallbackQuery) -> None:
    await callback_query.answer()
    items = await items_crud.get_items()
    await callback_query.message.edit_text(
        f"Существующие сейчас предметы:\n "
        f"{'\n'.join(map(str, [(item.id, item.data) for item in items]))}")
