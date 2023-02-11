from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from key_boards.inline.inline_kb_profile import ikb_profile_off, ikb_profile_on
from loader import dp

from filters import IsPrivate, IsActivate
from market import market_notific
from states import finding, change_price, change
from utils.db_api import quick_commands as commands, quick_commands, item_commands
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(), IsActivate(), text=['/profile', "Профиль"])
async def get_profile(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    if (user.notification == 'on'):
        await message.answer(f'Профиль <b>{message.from_user.first_name}</b>', reply_markup=ikb_profile_on)
    else:
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
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Изменить цену", callback_data=f'change price:{answer}'),
            InlineKeyboardButton(text="🗑 Удалить предмет", callback_data=f'delete one item:{answer}')
        ]
    ])
    await call.message.answer(f'Ослеживатся {item.item_name}\n'
                              f'По цене: {item.price}', reply_markup=markup)


@dp.callback_query_handler(text_startswith="delete one item")
async def change_price(call: types.CallbackQuery, state: FSMContext):
    answer = int(call.data.split(":")[1])
    await item_commands.delete_item(answer)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("🔙 Вернуться к моим пердметам", callback_data="my items")
        ]
    ])
    await call.message.answer('Предмет успешно удален',reply_markup=markup)


@dp.callback_query_handler(text_startswith="change price")
async def change_price(call: types.CallbackQuery, state: FSMContext):
    answer = int(call.data.split(":")[1])
    await state.update_data(id=answer)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("🚫 Отмена", callback_data="quit")
        ]
    ])
    await call.message.answer('Введите цену:',reply_markup=markup)
    await change.price.set()


@dp.message_handler(state=change.price)
async def get_price(message: types.Message, state: FSMContext):
    price = message.text
    check_price = await item_commands.correct_price(price)
    if (check_price):
        data = await state.get_data()
        id = data.get('id')
        print(id)
        await item_commands.change_price(int(id), float(price))
        await message.answer(f'Цена успешно изменена')
        await state.finish()
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton("🚫 Отмена", callback_data="quit")
            ]
        ])
        await message.answer('Некорректные данные',reply_markup=markup)


@dp.callback_query_handler(text="notifications")
async def change_notification(call: types.CallbackQuery):
    status = await quick_commands.change_notification(call.from_user.id)
    user = await quick_commands.select_user(call.from_user.id)
    current_markup = call.message.reply_markup
    print(status)
    print(user.notification)
    if status:
        if ikb_profile_off != current_markup:
            await call.message.edit_reply_markup(reply_markup=ikb_profile_off)
    elif not status:
        if ikb_profile_on != current_markup:
            await call.message.edit_reply_markup(reply_markup=ikb_profile_on)
            items = await item_commands.select_user_items(call.from_user.id)
            while (user.notification == 'on'):
                user = await quick_commands.select_user(call.from_user.id)
                await market_notific(items, call.message)
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
    answer = int(call.data.split(":")[1])
    await item_commands.delete_item(answer)
    items = await item_commands.select_user_items(call.from_user.id)
    buttons = [InlineKeyboardButton(text=item.item_name, callback_data=f'delete_item:{item.item_id}') for item in items]
    markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
    await call.message.answer('Выберите предмет который хотите удалить', reply_markup=markup)

@dp.callback_query_handler(text='quit', state=list(change.all_states_names))
async def quit_to_back(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

