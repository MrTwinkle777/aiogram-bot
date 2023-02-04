from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

end_register = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить регистрацию', callback_data='quit')
                                      ]
                                  ])