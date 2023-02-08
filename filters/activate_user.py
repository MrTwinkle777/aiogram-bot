from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import quick_commands


class IsActivate(BoundFilter):
    async def check(self, message: types.Message):
        user = await quick_commands.select_user(message.from_user.id)
        if user == None:
            await message.answer(text=f'Ошибка!!! Вы не зарегистрированы\n'
                                      f'Чтобы начать добавлять предметы нажмите команду /start')
            return False
        else:
            return True
