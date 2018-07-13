import os
import sys
import time
import copy
import datetime
from pprint import pprint
from operator import itemgetter
from collections import OrderedDict
sys.path.append(r"C:\dev\binance")
import binance

class Watcher:
    def __init__(self):
        self.tradingPairs = {}
        self.currencyObjects = []
        self.topCurrencies = {}

    def create_currency_objects(self):
        _priceData = self._get_price_data()
        for item in _priceData:
            _obj = Currency(pair=item["pair"], start_price=item["last"], start_time=item["last"])
            self.currencyObjects.append(_obj)

    def update_top_currencies(self):
        _data = {}
        for item in self._get_price_data():
            _pair = item["pair"]
            _price = item["last"]
            for obj in self.currencyObjects:
                if _pair == obj.pair:
                    _change = obj.check_price(price=_price)
                    _data.update({_pair: _change})

        _data = OrderedDict(sorted(_data.items(), key=itemgetter(1), reverse=True))

        self._format_top_items(data=_data)
        self.display_top_currencies()

    def _format_top_items(self, data):
        self.topCurrencies = {}
        _keys = list(data.keys())
        for i in range(0, 10):
            _pair = _keys[i]
            _change = data[_keys[i]]
            self.topCurrencies.update({_pair: _change})
        self.topCurrencies = OrderedDict(sorted(self.topCurrencies.items(), key=itemgetter(1), reverse=True))

    def display_top_currencies(self):
        print("Updated at {_time}".format(_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        print("="*100)
        for key, val in self.topCurrencies.items():
            print("pair: {pair}, price: {price}".format(pair=key, price=val))
        print("="*100)
        print("\n")
    def _get_price_data(self):
        return binance.get_price()

    def _get_trading_pairs(self):
        self.tradingPairs = binance.get_trading_pairs()


class Currency:
    def __init__(self, pair, start_price, start_time):
        self.pair = pair
        self.startPrice = start_price
        self.startTime = start_time
        self.percentageChange = ""

    def check_price(self, price):
        _startPrice = float(self.startPrice)
        _currentPrice = float(price)
        return str(get_percentage_difference(value1=_startPrice, value2=_currentPrice))


def get_difference(value1, value2):
    return float(value1) - float(value2)


def get_percentage_difference(value1, value2):
    difference = get_difference(value1=value1, value2=value2)
    average = float(value1) + float(value2) / 2

    return (difference / average) * 100

a = False
watcherObj = Watcher()
watcherObj.create_currency_objects()
while a is False:
    watcherObj.update_top_currencies()
    time.sleep(3600)
