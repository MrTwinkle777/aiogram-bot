from aiogram.dispatcher.filters.state import StatesGroup, State


class finding(StatesGroup):
    print_name = State()
    next = State()
    add_item = State()
    price = State()
