from aiogram import Dispatcher

from .private_chat import IsPrivate
from .activate_user import IsActivate



def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsActivate)