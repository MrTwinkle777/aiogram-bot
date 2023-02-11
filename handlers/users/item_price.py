from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from key_boards.default import kb_menu
from market import get_price_item_market
from filters import IsPrivate
from loader import dp
from states import finding
from utils.db_api import item_commands, quick_commands
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(), text="Цена предмета")
async def get_price(message: types.Message):
    await message.answer("Введите название предмета на латинице:")
    await finding.print_name.set()


@dp.callback_query_handler(text="add item")
async def get_price(call: types.CallbackQuery):
    await call.message.answer("Введите название предмета на латинице:")
    await finding.print_name.set()


@dp.message_handler(IsPrivate(), state=finding.print_name)
async def get_price(message: types.Message, state: FSMContext):
    answer = str(message.text)
    items = get_price_item_market(answer)
    if (items == {}):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton("🚫 Прекратить поиск", callback_data="quit")
            ]
        ])
        await message.answer('Предмета нет на маркете или название некорректно\n'
                             'Повторите попытку', reply_markup=markup)
    else:
        # for item, values in items.items():
        #     i = f'{item} : {values["price"]} руб.'
        #     await message.answer(i)
        buttons = [InlineKeyboardButton(text=item, callback_data=f'item:{item}') for item in
                   dict(list(items.items())[:6])]
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
        markup.add(
            InlineKeyboardButton("PREV", callback_data=f"prev:0"),
            InlineKeyboardButton(str(0), callback_data="null"),
            InlineKeyboardButton("NEXT", callback_data=f"next:0"),
        )
        markup.add(
            InlineKeyboardButton("🚫 Прекратить поиск", callback_data="quit"),
        )
        await message.answer('Вот что удалось найти', reply_markup=markup)
        await state.update_data(items=items)
        await finding.next.set()


@dp.callback_query_handler(text_startswith="prev", state=finding.next)
async def prev_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = int(call.data.split(":")[1]) - 1
    items = await state.get_data('items')
    items = items['items']
    buttons = [InlineKeyboardButton(text=item, callback_data=f'item:{item}') for item in
               dict(list(items.items())[data * 6:(6 * (data + 1))])]
    if data >= 0:
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
        markup.add(
            InlineKeyboardButton("PREV", callback_data=f"prev:{data}"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton("NEXT", callback_data=f"next:{data}"),
        )
    else:
        data = int(call.data.split(":")[1])
        buttons = [InlineKeyboardButton(text=item, callback_data=f'item:{item}') for item in
                   dict(list(items.items())[data * 6:(6 * (data + 1))])]
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
        markup.add(
            InlineKeyboardButton("PREV ❌", callback_data="null"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton("NEXT", callback_data=f"next:{data}"),
        )
    markup.add(
        InlineKeyboardButton("🚫 Прекратить поиск", callback_data="quit"),
    )
    await call.message.edit_text(text='Вот что удалось найти', reply_markup=markup)
    await finding.next.set()


@dp.callback_query_handler(text_startswith="next", state=finding.next)
async def next_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = int(call.data.split(":")[1]) + 1
    items = await state.get_data()
    items = items.get('items')
    buttons = [InlineKeyboardButton(text=item, callback_data=f'item:{item}') for item in
               dict(list(items.items())[data * 6:(6 * (data + 1))])]
    if (6 * data) + 1 < len(items):
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
        markup.add(
            InlineKeyboardButton("PREV", callback_data=f"prev:{data}"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton("NEXT", callback_data=f"next:{data}"),
        )
    else:
        data = int(call.data.split(":")[1])
        buttons = [InlineKeyboardButton(text=item, callback_data=f'item:{item}') for item in
                   dict(list(items.items())[data * 6:(6 * (data + 1))])]
        markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 1] for i in range(0, len(buttons), 1)])
        markup.add(
            InlineKeyboardButton("PREV", callback_data=f"prev:{data}"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton(text="NEXT ❌", callback_data="null")
        )
    markup.add(
        InlineKeyboardButton("🚫 Прекратить поиск", callback_data="quit"),
    )
    await call.message.edit_text(text='Вот что удалось найти', reply_markup=markup)
    await finding.next.set()


@dp.callback_query_handler(text_startswith="item", state=finding.next)
async def get_5_news(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    answer = str(call.data.split(":")[1])
    """Попробовать что нибудь еще"""
    item = get_price_item_market(answer)
    await state.update_data(name=answer)
    price = item[answer]['price']
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Добавить в список отслеживаемого"),  ##Подредачить может добавить больше описания
                KeyboardButton(text="Вернуться к выбору")
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await call.message.answer(f'Предмет: {answer}\n'
                              f'Цена на маркете: {price} ', reply_markup=markup)
    await finding.add_item.set()


@dp.message_handler(IsPrivate(), text="Добавить в список отслеживаемого", state=finding.add_item)
async def add_item_name(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    if user is not None:
        data = await state.get_data()
        name = data.get('name')
        await message.answer(text=f'Выбранный предмет:\n'
                                  f'{name}')
        await message.answer(text='Введите цену:')
        await finding.price.set()
    else:
        await message.answer(f'Ошибка!!! Вы не зарегистрированы\n'
                             f'Чтобы начать добавлять предметы нажмите команду /start')
        await state.finish()


@dp.message_handler(IsPrivate(), text="Вернуться к выбору", state=finding.add_item)
async def go_back(message: types.Message, state: FSMContext):
    await message.delete()
    await finding.next.set()


@dp.message_handler(IsPrivate(), state=finding.price)
async def add_item_name(message: types.Message, state: FSMContext):
    price = message.text
    check_price = await item_commands.correct_price(price)
    if (check_price):
        data = await state.get_data()
        name = data.get('name')
        await item_commands.add_item(user_id=message.from_user.id,
                                     item_name=name,
                                     price=float(price))
        await message.answer(f'Предмет успешно добавлен')
        await state.finish()
    else:
        await message.answer('Некорректные данные')


@dp.callback_query_handler(text='quit', state=list(finding.all_states_names))
async def quit_to_back(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(text='Поиск прекращен',reply_markup=kb_menu)
