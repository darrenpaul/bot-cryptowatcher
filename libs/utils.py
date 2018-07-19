from operator import itemgetter
from collections import OrderedDict

def sort_data(data, reverse=True):
    for key, val in data.items():
        data[key] = OrderedDict(sorted(data[key].items(), key=itemgetter(1), reverse=True))
    return data
