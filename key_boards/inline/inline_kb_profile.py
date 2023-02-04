from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_profile_on = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='🗂 Мои предметы', callback_data='my items')
                                      ],
[
                                          InlineKeyboardButton(text='🔔 Уведомления', callback_data='notifications')
                                      ],
                                      [
                                          InlineKeyboardButton(text="➕ Добавить предмет",callback_data='add item'),
                                          InlineKeyboardButton(text="🗑 Удалить предмет",callback_data='delete item'),
                                      ]
                                  ])

ikb_profile_off = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='🗂 Мои предметы', callback_data='my items')
                                      ],
[
                                          InlineKeyboardButton(text='🔕 Уведомления', callback_data='notifications')
                                      ],
                                      [
                                          InlineKeyboardButton(text="➕ Добавить предмет",callback_data='add item'),
                                          InlineKeyboardButton(text="🗑 Удалить предмет",callback_data='delete item'),
                                      ]
                                  ])