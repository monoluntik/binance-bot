import logging
from aiogram import Bot, Dispatcher, types, executor
import pdb
import asyncio


from config import (
    token,
)  # Токен бота, я сохранил в файле, файл находится в .gitignore
from pars_binance import PriceUSDT


bot = Bot(token=token)

dp = Dispatcher(bot=bot)
logging.basicConfig(level=logging.INFO)

users_list = []

DELAY = 5

buttons = [
    "LTC",
    "BTC",
    "ETH",
    "ADA",
    "VET",
    "SOL",
    "LUNA",
    "BNB",
]


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    s = PriceUSDT(id=message.chat.id)

    for user in users_list:
        if user.id == message.chat.id:
            users_list.pop(users_list.index(user))
    users_list.append(s)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer("Выберите крипту", reply_markup=keyboard)


@dp.message_handler(commands=["stop"])
async def send_by(message: types.Message):
    for user in users_list:
        if user.id == message.chat.id:
            user.deactivate()
            await message.reply(f"Stop {user.coin}")


@dp.message_handler()
async def with_puree(message: types.Message):

    if not message.text in buttons:
        await message.reply("Я тебя не понимаю. Напиши /start")
        return

    for user in users_list:

        if user.id != message.chat.id:
            continue

        user.set_coin(message.text)
        if not user.status:
            user.activate()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            butt = ["/stop", "/start"]
            keyboard.add(*butt)
            await message.reply(f"Start {user.coin}", reply_markup=keyboard)


async def send_messsage():
    for user in users_list:
        if user.status != []:
            new_message = user.get_message()
            await dp.bot.send_message(user.id, new_message)


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, send_messsage, loop)
    executor.start_polling(dp, loop=loop)
