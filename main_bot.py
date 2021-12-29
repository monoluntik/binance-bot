import logging
from aiogram import Bot, Dispatcher, types, executor

import asyncio


from config import token # Токен бота, я сохранил в файле, файл находится в .gitignore
from pars_binance import GetPriceUSDT


bot = Bot(token=token)

dp = Dispatcher(bot=bot)
logging.basicConfig(level=logging.INFO)

liiist = []

DELAY = 30

buttons = ["LTC", "BTC", "ETH", "ADA", "VET", "SOL", "LUNA", "BNB",]
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    s = GetPriceUSDT(id = message.chat.id)
    for i in liiist:
        if i.id == message.chat.id:
            liiist.pop(liiist.index(i))
    liiist.append(s)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer("Выберите крипту", reply_markup=keyboard)

@dp.message_handler(commands=['stop'])
async def send_by(message: types.Message):
    for i in liiist:
        if i.id == message.chat.id:
            i.deactivate()
            await message.reply(f"Stop {i.coin}")

@dp.message_handler()
async def with_puree(message: types.Message):
    if message.text in buttons:
        for i in liiist:
            if i.id == message.chat.id:
                i.set_coin(message.text)
                if i.list_ == []:
                    i.activate()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    butt = ["/stop", "/start"]
                    keyboard.add(*butt)
                    await message.reply(f"Start {i.coin}", reply_markup=keyboard)
    else:
        await message.reply("Я тебя не понимаю. Напиши /start")
    

async def send_price():
    for i in liiist:
        if i.list_ != []:
            new_message = i.get_message()
            id = i.id
            if new_message != "Измеменений нет!":
                await dp.bot.send_message(id, new_message)


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, send_price, loop)
    executor.start_polling(dp, loop=loop)