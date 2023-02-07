from aiogram import types


from key_boards.default import kb_menu

from loader import dp

from filters import IsPrivate
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(), text=['/menu', "Меню"])
async def command_menu(message: types.Message):
    await message.answer('Выберите действие', reply_markup=kb_menu)
