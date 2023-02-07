from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(user_id: int, notification='off'):
    try:
        user = User(user_id=user_id,notification=notification)
        await user.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def change_notification(user_id):
    user = await select_user(user_id)
    try:
        status = user.notification
        if status == 'on':
            await user.update(notification='off').apply()
            return True
        elif status == 'off':
            await user.update(notification='on').apply()
            return False
    except Exception:
        pass

# async def update_status(user_id, new_status):
#     user = await select_user(user_id)
#     await user.update(status=new_status).apply()


# async def check_args(args, user_id):
#     if args == '':
#         args = '0'
#         return args
#     elif not args.isnumeric():
#         args = '0'
#         return args
#     elif args.isnumeric():
#         if int(args) == user_id:
#             args = '0'
#             return args
#         elif await select_user(user_id=int(args)) is None:
#             args = '0'
#             return args
#         else:
#             args = str(args)
#             return args
#     else:
#         args = '0'
#         return args
#
#
# async def count_refs(user_id):
#     refs = await User.query.where(User.referral_id == user_id).gino.all()
#     return len(refs)


# async def new_balance(user_id: int, amount):
#     user = await select_user(user_id)
#     new_user_balance = round((user.balance + amount),2)
#     print(new_user_balance)# Проверить
#     await user.update(balance=new_user_balance).apply()


# async def add_price_balance(user_id: int,item_name:str, amount):
#     item = await select_user(user_id)
#     try:
#         amount = float(amount)
#         if (user.balance + amount) >= 0 and (str(amount).split(".")[1].__len__() <= 2):
#             await new_balance(user_id, amount)
#             return True, format(user.balance + amount, '.2f')
#         elif user.balance + amount < 0:
#             return 'no money', 0
#         else:
#             return (False,
#                     f'Некорректное число\n' \
#                     f'Повторите попытку')
#
#     except Exception:
#         return (False,
#                 f'Некорректное число\n' \
#                 f'Повторите попытку')
