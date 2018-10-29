import os
import sys
import time
import copy
import datetime
from pprint import pprint
from operator import itemgetter
from collections import OrderedDict
from . import utils
from . import wallet
from . import currency
from libs.binance import binance


class Watcher:
    def __init__(self):
        self.wallet = wallet.Wallet()
        self.tradingPairs = self._get_trading_pairs()
        self.currencyObjects = []
        self._pairs = []
        self.topCurrencies = {}

    def create_currency_objects(self):
        for item in self._get_price_data():
            _obj = currency.Currency(currency_data=item)
            setattr(self.wallet, item["pair"], _obj)
            self.currencyObjects.append(_obj)

    def update_top_currencies(self):
        _data = {}
        self._pairs = []

        for item in self._get_price_data():
            _pair = item["pair"]
            _price = item["last"]
            _volume = item["volume"]
            if hasattr(self.wallet, _pair):
                _obj = getattr(self.wallet, _pair)
                _change = _obj.check_price(price=_price)
                _obj.check_volume(volume=_volume)
                _data.update({_pair: _change})

        _data = self._pair_currencies(data=_data)

        _data = utils.sort_data(data=_data)

        self._get_top_currencies(_data)

    def display_top_currencies(self, base_currency, data):
        _ignores = ["BNB", "USDT"]
        self._add_pairs(pairs=list(data.keys()))
        if base_currency not in _ignores:
            print("="*100)
            print("Base currency {base}".format(base=str(base_currency)))
            print("Updated at {_time}".format(_time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))))
            print("="*100)
            for key, val in data.items():
                self._add_frequency(pair=key)
                _candle = binance.get_candle_stick(pair=key, interval="4h")
                _candeChange = get_percentage_change(new_value=float(_candle["close"]), original_value=float(_candle["open"]))
                print("Trading pair: {pair}".format(pair=str(key)))
                print("Price Change: {change}%".format(change=str(val)))
                print("Price: {start} -> {current}".format(start=str(getattr(self.wallet, key).startPrice), current=str(getattr(self.wallet, key).lastPrice)))
                print("Highest Price: {price}".format(price=str(getattr(self.wallet, key).highestPrice)))
                print("Candle {opn} -> {cls}".format(opn=str(_candle["open"]), cls=_candle["close"]))
                print("Candle Change {chg}%".format(chg=str(_candeChange)))
                print("Volume: {start} -> {current}".format(start=str(getattr(self.wallet, key).startVolume), current=str(getattr(self.wallet, key).lastVolume)))
                print("Volume Change: {change}%".format(change=str(getattr(self.wallet, key).volumeChange)))
                print("Frequency: {freq}".format(freq=str(getattr(self.wallet, key).frequency)))
                print("Total Frequency: {freq}".format(freq=str(getattr(self.wallet, key).totalFrequency)))
                print("-"*100)
            print("="*100)
            print("\n")

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

    def _get_top_currencies(self, data, amount=10):
        for bse, val in data.items():
            _topPeformers = {}
            _keys = list(val.keys())
            for ind in range(0, amount):
                _pair = _keys[ind]
                _change = val[_pair]
                _topPeformers.update({_pair: _change})
            self.display_top_currencies(base_currency=bse, data=_topPeformers)

    def _add_pairs(self, pairs):
        self._pairs = self._pairs + pairs

    def _update_currency_frequencies(self):
        for currency in self.currencyObjects:
            if currency.pair not in self._pairs:
                currency.frequency = 0

    def _get_price_data(self):
        return binance.get_price()

    def _get_trading_pairs(self):
        return copy.deepcopy(binance.get_trading_pairs())

    def _add_frequency(self, pair):
        getattr(self.wallet, pair).frequency += 1
        getattr(self.wallet, pair).totalFrequency += 1


def get_difference(value1, value2):
    return float(value1) - float(value2)


def get_percentage_change(new_value, original_value):
    difference = get_difference(value1=new_value, value2=original_value)

    return (difference / original_value) * 100
