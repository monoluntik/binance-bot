import requests

import json
from datetime import datetime


class PriceUSDT:
    def __init__(self, id):
        self.status = []
        self.coin = None
        self.id = id

    def set_coin(self, coin):
        self.coin = coin
        self.old_price = self.get_bnb_price()
        self.old_time = datetime.now()

    def activate(self):
        self.status.append(self)

    def deactivate(self):
        self.list_.clear()

    def get_bnb_price(self):
        if self.coin != None:
            symbol = self.coin
            URL = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            responce = requests.get(
                URL, headers={"User-agent": "your bot 0.1"}
            )
            json_obj = responce.text
            python_obj = json.loads(json_obj)
            a = python_obj.get("price")
            k = float(a)
            return round(k, 2)

    def get_message(self):
        new_price = self.get_bnb_price()
        new_time = datetime.now()
        if round(new_price - self.old_price, 2) != 0:
            new_message = f"""{self.coin}\nOld price: {self.old_price}\n{self.old_time}
            \nNew price: {new_price}\n{new_time}
            \n{"The price fell by" if new_price < self.old_price else "The price went up by"}: 
            {round(abs(new_price-self.old_price), 2)}"""
            self.old_price = new_price
            self.old_time = new_time
            return new_message
        return f"Измеменений нет!"
