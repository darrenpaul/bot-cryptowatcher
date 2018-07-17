import os
import sys
import time
import copy
import datetime
from pprint import pprint
from operator import itemgetter
from collections import OrderedDict
from . import currency
from . import wallet
from libs.binance import binance


class Watcher:
    def __init__(self):
        self.wallet = wallet.Wallet()
        self.tradingPairs = self._get_trading_pairs()
        self.currencyObjects = []
        self.topCurrencies = {}

    def create_currency_objects(self):
        for item in self._get_price_data():
            _obj = currency.Currency(currency_data=item)
            setattr(self.wallet, item["pair"], _obj)
            self.currencyObjects.append(_obj)

    def update_top_currencies(self):
        _data = {}

        for item in self._get_price_data():
            _pair = item["pair"]
            _price = item["last"]
            _volume = item["volume"]
            for obj in self.currencyObjects:
                if _pair == obj.pair:
                    _change = obj.check_price(price=_price)
                    obj.check_volume(volume=_volume)
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
        _ignores = ["BNB", "USDT"]
        self._update_currency_frequencies(pairs=data.keys())

        if base_currency not in _ignores:
            print("="*100)
            print("Base currency {base}".format(base=base_currency))
            print("Updated at {_time}".format(_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            print("="*100)
            for key, val in data.items():
                getattr(self.wallet, key).frequency += 1
                getattr(self.wallet, key).totalFrequency += 1
                _candle = binance.get_candle_stick(pair=key, interval="4h")["close"]
                print("Trading pair: {pair}".format(pair=key))
                print("Price Change: {change}%".format(change=val))
                print("Price: {start} -> {current}".format(start=getattr(self.wallet, key).startPrice, current=getattr(self.wallet, key).lastPrice))
                print("Highest Price: {price}".format(price=getattr(self.wallet, key).highestPrice))
                print("Candle Close {cdl}".format(cdl=_candle))
                print("Volume: {start} -> {current}".format(start=getattr(self.wallet, key).startVolume, current=getattr(self.wallet, key).lastVolume))
                print("Volume Change: {change}%".format(change=getattr(self.wallet, key).volumeChange))
                print("Frequency: {freq}".format(freq=getattr(self.wallet, key).frequency))
                print("Total Frequency: {freq}".format(freq=getattr(self.wallet, key).totalFrequency))
                print("-"*100)
            print("="*100)
            print("\n")

    def _update_currency_frequencies(self, pairs):
        for currency in self.currencyObjects:
            if currency.pair not in pairs:
                currency.frequency = 0

    def _get_price_data(self):
        return binance.get_price()

    def _get_trading_pairs(self):
        return copy.deepcopy(binance.get_trading_pairs())
