import os
import sys
from pprint import pprint
sys.path.append(r"C:\dev\binance")
import binance

class Watcher:
    def __init__(self):
        self.tradingPairs = {}
        self.currencyObjects = []

    def create_currency_objects(self):
        _priceData = self._get_price_data()

    def _get_price_data(self):
        return binance.get_price()

    def _get_trading_pairs(self):
        self.tradingPairs = binance.get_trading_pairs()


class Currency:
    def __init__(self, start_price, start_time):
        self.startPrice = ""
        self.startTime = ""
        self.lastPrice = ""
        self.lastTime = ""
        self.percentageChange = ""

    def add_price(self, current_price, current_time):
        _startPrice = float(self.startPrice)
        _currentPrice = float(current_price)

        print get_percentage_difference(value1=_startPrice, value2=_currentPrice)


def get_difference(value1, value2):
    return float(value1) - float(value2)


def get_percentage_difference(value1, value2):
    difference = get_difference(value1=value1, value2=value2)
    average = float(value1) + float(value2) / 2

    return (difference / average) * 100

a = False
watcherObj = Watcher()
while a is False:
    watcherObj.create_currency_objects()
