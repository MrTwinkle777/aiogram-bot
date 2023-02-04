from aiogram import types

from filters import IsPrivate
from loader import dp
from utils.db_api import quick_commands
from utils.misc import rate_limit


@rate_limit(limit=1)
@dp.message_handler(IsPrivate(), text=['/register','Зарегистрироваться'])
async def register_user(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    if user is None:
        await quick_commands.add_user(message.from_user.id)
    await message.answer(f'Регистрация прошла успешно \n')


#
# @dp.message_handler(IsPrivate(), state=register.name)
# async def get_name(message: types.Message, state: FSMContext):
#     answer = message.text
#
#     await state.update_data(name=answer)
#     await message.answer('Введите свой номер телефона:', reply_markup=end_register)
#     await register.phone.set()
#
#
# @dp.message_handler(IsPrivate(), state=register.phone)
# async def get_phone(message: types.Message, state: FSMContext):
#     answer = message.text
#
#     await state.update_data(phone=answer)
#     await message.answer(f'Введите свой возраст', reply_markup=end_register)
#     await register.age.set()
#
#
# @dp.message_handler(IsPrivate(), state=register.age)
# async def get_age(message: types.Message, state: FSMContext):
#     answer = message.text
#     if answer.isnumeric():
#         if 150 > int(answer) > 0:
#             await state.update_data(age=answer)
#             data = await state.get_data()
#             name = data.get('name')
#             phone = data.get('phone')
#             age = data.get('age')
#             await register_commands.new_registration(user_id=message.from_user.id,
#                                                      tg_name=name,
#                                                      phone=phone,
#                                                      age=age,
#                                                      status='accepted')
#             await message.answer(f'Регистрация завершена\n'
#                                  f'Имя: {name}\n'
#                                  f'Возраст: {age}\n'
#                                  f'Номер телевона: {phone}')
#         else:
#             await message.answer(f'Введите корректный возраст', reply_markup=end_register)
#     else:
#         await message.answer(f'Введите корректный возраст', reply_markup=end_register)
#
# @dp.callback_query_handler(text='quit', state=[register.name, register.phone, register.age])
# async def quit(call: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await call.message.answer('Регистрация прервана')
#
