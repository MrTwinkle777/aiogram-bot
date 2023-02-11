import asyncio
import json


async def market_notific(items, message):
    while True:
        try:
            with open(r"./market/market_items.json", "r") as file:
                data = json.load(file)
            break
        except FileNotFoundError:
            pass
            # print("The file was not found. Please check the file path and try again.")
        except json.JSONDecodeError:
            pass
            # print("The file could not be parsed as a JSON file. Please check the file format and try again.")

    await asyncio.sleep(1)
    for item in items:
        name = item.item_name
        price = item.price
        print(float(data[name]['price']))
        if (float(data[name]['price']) < price):
            await message.answer(text=f'Появился {name} \n'
                                      f'''По цене {float(data[name]['price'])} рублей''')
        print(name)
        print(price)
        # print(data)
