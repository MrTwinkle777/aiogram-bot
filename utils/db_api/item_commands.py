from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.items import Items


async def add_item(user_id: int, item_name: str, price: float, ):
    try:
        item = Items(user_id=user_id, item_name=item_name, price=price)
        await item.create()
    except UniqueViolationError:
        print('Предмет не добавлен')


async def select_item(item_id):
    item = await Items.query.where(Items.item_id == item_id).gino.first()
    return item


async def select_user_items(user_id):
    items = await Items.query.where(Items.user_id == user_id).gino.all()
    return items


async def correct_price(price):
    try:
        price = float(price)
        if (str(price).split(".")[1].__len__() <= 2) and (1000000 > price > 0):
            return True
        else:
            return False
    except Exception:
        return False


async def change_price(item_id: int, price):
    item = await select_item(item_id)
    try:
        price = float(price)
        if (str(price).split(".")[1].__len__() <= 2) and (1000000 > price > 0):
            await item.update(price=price).apply()
            return (True, f'Цена успешна изменена\n' \
                          f'В данный момент отслеживаемая цена {price}')
        else:
            return (False,
                    f'Некорректное число\n' \
                    f'Повторите попытку')

    except Exception:
        return (False,
                f'Некорректное число\n' \
                f'Повторите попытку')
