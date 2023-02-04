from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Цена предмета"), ##Подредачить может добавить больше описания
            KeyboardButton(text="Зарегистрироваться" )
        ],
        [
            KeyboardButton(text="Профиль"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)