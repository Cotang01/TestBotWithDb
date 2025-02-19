from aiogram.utils.keyboard import InlineKeyboardBuilder


builder = InlineKeyboardBuilder()
builder.button(text='Показать существующие предметы',
               callback_data='show_items_callback')
