from aiogram import types

# list of items
items = ["Приветствую тебя в боте-помощнике по MarketCsGo", "Приветствую тебя в боте-помощнике по MarketCsGo", "item 3", "item 3","item 3","item 3","item 3","item 3","item 3","item 3","item 3","item 3",
"item 3","item 3","item 3","item 3","item 3","item 3","item 3","item 20"]

# create inline keyboard buttons for each item
buttons = [types.InlineKeyboardButton(text=item, callback_data=item) for item in items]

# divide buttons into two parts
part1 = buttons[:10]
part2 = buttons[10:]

# create inline keyboard markup for part 1
keyboard1 = types.InlineKeyboardMarkup(inline_keyboard=[part1[i:i + 2] for i in range(0, len(part1), 1)])

# create inline keyboard markup for part 2
keyboard2 = types.InlineKeyboardMarkup(inline_keyboard=[part2[i:i + 2] for i in range(0, len(part2), 2)])

# create navigation buttons
next_page = types.InlineKeyboardButton(text="Next", callback_data="next_page")
prev_page = types.InlineKeyboardButton(text="Prev", callback_data="prev_page")

# add navigation buttons to each inline keyboard
keyboard1.inline_keyboard.append([next_page])
keyboard2.inline_keyboard.insert(0, [prev_page])
