from aiogram import types

from key_boards.inline.inline_kb_profile import ikb_profile_off
from loader import dp

from filters import IsPrivate
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(), text=['/profile',"Профиль"])
async def get_profile(message: types.Message):
    await message.answer(f'Профиль <b>{message.from_user.first_name}</b>',reply_markup=ikb_profile_off)


