import os
import sys
import time
import copy
import datetime
from pprint import pprint
from operator import itemgetter
from collections import OrderedDict
sys.path.append(r"C:\Users\darre\Documents\development\binance")
import binance


class Watcher:
    def __init__(self):
        self.wallet = Wallet()
        self.tradingPairs = self._get_trading_pairs()
        self.currencyObjects = []
        self.topCurrencies = {}

    def create_currency_objects(self):
        for item in self._get_price_data():
            _obj = Currency(pair=item["pair"], start_price=item["last"], start_time=item["last"])
            self.wallet
            setattr(self.wallet, item["pair"], _obj)
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

        _data = self._pair_currencies(data=_data)

        for key, val in _data.items():
            _data[key] = OrderedDict(sorted(_data[key].items(), key=itemgetter(1), reverse=True))

        for key, val in _data.items():
            self._format_top_items(base_currency=key, data=val)

    def _pair_currencies(self, data):
        _data = {}
        for key, val in self.tradingPairs.items():
            _base = key
            for quote in val:
                _pair = "{quote}{base}".format(quote=quote, base=_base)
                for pair, per in data.items():
                    if pair == _pair:
                        if _base not in _data.keys():
                            _data.update({_base: {}})
                        _data[_base].update({pair: per})
        return _data

    def _format_top_items(self, base_currency, data):
        _topCurrencies = {}
        _keys = list(data.keys())
        for i in range(0, 10):
            _pair = _keys[i]
            _change = data[_keys[i]]
            _topCurrencies.update({_pair: _change})
        _topCurrencies = OrderedDict(sorted(_topCurrencies.items(), key=itemgetter(1), reverse=True))
        self.display_top_currencies(base_currency=base_currency, data=_topCurrencies)

    def display_top_currencies(self, base_currency, data):
        print("="*100)
        print("Base currency {base}".format(base=base_currency))
        print("Updated at {_time}".format(_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        print("="*100)
        for key, val in data.items():
            print("Trading pair: {pair}".format(pair=key))
            print("Change: {change}".format(change=val))
            print("Price: {start} -> {current}".format(start=getattr(self.wallet, key).startPrice, current=getattr(self.wallet, key).lastPrice))
            print("Occurence: {occurence}".format(occurence=getattr(self.wallet, key).occurence))
            print("-"*100)
        print("="*100)
        print("\n")

    def _get_price_data(self):
        return binance.get_price()

    def _get_trading_pairs(self):
        return copy.deepcopy(binance.get_trading_pairs())


class Currency:
    def __init__(self, pair, start_price, start_time):
        self.pair = pair
        self.startPrice = start_price
        self.startTime = start_time
        self.lastPrice = ""
        self.occurence = 0

    def check_price(self, price):
        self.lastPrice = price
        _startPrice = float(self.startPrice)
        _currentPrice = float(self.lastPrice)
        self.occurence += 1
        return str(get_percentage_change(new_value=_currentPrice, original_value=_startPrice))


class Wallet:
    def __init__(self):
        pass


def get_difference(value1, value2):
    return float(value1) - float(value2)


def get_percentage_change(new_value, original_value):
    difference = get_difference(value1=new_value, value2=original_value)

    return (difference / original_value) * 100

a = False
watcherObj = Watcher()
watcherObj.create_currency_objects()
while a is False:
    watcherObj.update_top_currencies()
    time.sleep(1800)
