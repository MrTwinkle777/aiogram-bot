from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from key_boards.default import kb_menu

from loader import dp

from filters import IsPrivate
from utils.db_api import item_commands
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(), text=['/menu', "Меню"])
async def command_menu(message: types.Message):
    await message.answer('Выберите действие', reply_markup=kb_menu)


@dp.callback_query_handler(text='my items')
async def print_items(call: types.CallbackQuery):
    items = await item_commands.select_user_items(call.from_user.id)
    buttons = [InlineKeyboardButton(text=item.item_name, callback_data=f'my_item:{item.item_id}') for item in items]
    markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
    await call.message.answer('Отслеживаемые предметы', reply_markup=markup)

@dp.callback_query_handler(text_startswith="my_item")
async def print_items(call: types.CallbackQuery):
    answer = str(call.data.split(":")[1])
    item = await item_commands.select_item(int(answer))
    await call.message.answer(f'Ослеживатся {item.item_name}\n'
                              f'По цене: {item.price}')