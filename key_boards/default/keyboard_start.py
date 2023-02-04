from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Цена предмета"), ##Подредачить может добавить больше описания
            KeyboardButton(text="Зарегистрироваться" )
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)