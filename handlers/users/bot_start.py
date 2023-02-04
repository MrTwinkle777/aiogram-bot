from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from key_boards.default import kb_start

from loader import dp

from filters import IsPrivate
from utils.db_api import quick_commands
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    if user is None:
        await quick_commands.add_user(message.from_user.id)
    await message.answer('Приветствую тебя в боте-помощнике по MarketCsGo\n'
                         'Выберите с чего вы хотите начать', reply_markup=kb_start)
