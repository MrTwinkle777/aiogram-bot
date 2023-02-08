from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from key_boards.inline.inline_kb_profile import ikb_profile_off, ikb_profile_on
from loader import dp

from filters import IsPrivate, IsActivate
from market import market_notific
from utils.db_api import quick_commands as commands, quick_commands, item_commands
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(),IsActivate(), text=['/profile', "Профиль"])
async def get_profile(message: types.Message):
    await message.answer(f'Профиль <b>{message.from_user.first_name}</b>', reply_markup=ikb_profile_off)


@dp.callback_query_handler(text='my items')
async def print_items(call: types.CallbackQuery):
    items = await item_commands.select_user_items(call.from_user.id)
    if len(items) > 0:
        buttons = [InlineKeyboardButton(text=item.item_name, callback_data=f'my_item:{item.item_id}') for item in items]
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
        await call.message.answer('Отслеживаемые предметы', reply_markup=markup)
    else:
        await call.message.answer('Нет отслеживаемых предметов')


@dp.callback_query_handler(text_startswith="my_item")
async def print_items(call: types.CallbackQuery):
    answer = str(call.data.split(":")[1])
    item = await item_commands.select_item(int(answer))
    await call.message.answer(f'Ослеживатся {item.item_name}\n'
                              f'По цене: {item.price}')


@dp.callback_query_handler(text="notifications")
async def change_notification(call: types.CallbackQuery):
    status = await quick_commands.change_notification(call.from_user.id)
    user = await quick_commands.select_user(call.from_user.id)
    print(status)
    print(user.notification)
    if status:
        await call.message.edit_reply_markup(reply_markup=ikb_profile_off)
    elif not status:
        print('dwad')
        await call.message.edit_reply_markup(reply_markup=ikb_profile_on)
        items = await item_commands.select_user_items(call.from_user.id)
        while (user.notification == 'on'):
            user = await quick_commands.select_user(call.from_user.id)
            await market_notific(items,call.message)
    else:
        await call.message.answer(f'Ошибка!!! Вы не зарегистрированы\n'
                                  f'Чтобы начать добавлять предметы нажмите команду /start')


@dp.callback_query_handler(text="delete items")
async def deleteting(call: types.CallbackQuery):
    items = await item_commands.select_user_items(call.from_user.id)
    if len(items) > 0:
        buttons = [InlineKeyboardButton(text=item.item_name, callback_data=f'delete_item:{item.item_id}') for item in
                   items]
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
        await call.message.answer('Выберите предмет который хотите удалить', reply_markup=markup)
    else:
        await call.message.answer('Нет отслеживаемых предметов')


@dp.callback_query_handler(text_startswith="delete_item")
async def delete_users_item(call: types.CallbackQuery):
    answer = str(call.data.split(":")[1])
    # item = await item_commands.select_item(int(answer))
    await item_commands.delete_item(int(answer))
    items = await item_commands.select_user_items(call.from_user.id)
    buttons = [InlineKeyboardButton(text=item.item_name, callback_data=f'delete_item:{item.item_id}') for item in items]
    markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
    await call.message.answer('Выберите предмет который хотите удалить', reply_markup=markup)
