import asyncio
import time

import requests
import json


def get_price_item_market(name):
    with open("./market/market_items.json") as file:
        data = json.load(file)
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
        with open("./market/market_items.json", 'w', encoding='utf-8') as file:
            json.dump(items_market, file)
    except Exception as ex:
        print(ex)
        pass


def find_item():
    while True:
        time.sleep(0.2)
        print('fff')
        get_market_price()
    # name = 'Desert Eagle'
    # items = get_price_item_market(name)
    # for item, values in items.items():
    #     print(f'{item} : {values}')


if __name__ == "__main__":
    find_item()
