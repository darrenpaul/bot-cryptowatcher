from pprint import pprint


class Currency:
    def __init__(self, currency_data):
        self.__set_attributes(data=currency_data)

    def check_price(self, price):
        self.lastPrice = str(price)
        _startPrice = float(self.startPrice)
        _currentPrice = float(self.lastPrice)
        self._check_for_highest_price()
        return str(get_percentage_change(new_value=_currentPrice, original_value=_startPrice))

    def check_volume(self, volume):
        self.lastVolume = volume
        _startVolume = float(self.startVolume)
        _currentVolume = float(self.lastVolume)
        self.volumeChange = str(get_percentage_change(new_value=_currentVolume, original_value=_startVolume))

    def _check_for_highest_price(self):
        _highestPrice = float(self.highestPrice)
        _lastPrice = float(self.lastPrice)
        if _lastPrice > _highestPrice:
            self.highestPrice = str(_lastPrice)

    def __set_attributes(self, data):
        self.pair = data["pair"]
        self.startPrice = str(data["last"])
        self.startTime = data["time"]
        self.startVolume = str(data["volume"])
        self.highestPrice = str(data["last"])
        self.lastPrice = None
        self.lastVolume = None
        self.volumeChange = None
        self.frequency = 0
        self.totalFrequency = 0


def get_difference(value1, value2):
    return float(value1) - float(value2)


def get_percentage_change(new_value, original_value):
    difference = get_difference(value1=new_value, value2=original_value)

    return (difference / original_value) * 100
