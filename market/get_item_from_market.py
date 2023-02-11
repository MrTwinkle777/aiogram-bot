import asyncio
import time

import requests
import json


def get_price_item_market(name):
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
    try:
        return {item: values for item, values in data.items() if name in item}
    except:
        return 0


def get_market_price():
    # name = name.replace('&', '%26').replace('o/F', 'o-F')
    try:
        link = f'https://market.csgo.com/api/v2/prices/RUB.json'
        response = requests.get(link).json()
        items = response['items']
        items_market = {}
        for item in items:
            name = item['market_hash_name']
            price = item['price']
            items_market[name] = {'price': price}
        with open(r"./market/market_items.json", 'w', encoding='utf-8') as file:
            json.dump(items_market, file)
    except Exception as ex:
        print(f'Ошибка {ex}')
        pass


def find_item():
    while True:
        time.sleep(0.2)
        get_market_price()
    # name = 'Desert Eagle'
    # items = get_price_item_market(name)
    # for item, values in items.items():
    #     print(f'{item} : {values}')


if __name__ == "__main__":
    get_market_price()
